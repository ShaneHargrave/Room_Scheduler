document.addEventListener('DOMContentLoaded', function () {
    let currentDate = new Date();
    let currentMonth = currentDate.getMonth();
    let currentYear = currentDate.getFullYear();

    let calendarData = [];
    let eventsByDay = {};

    const monthNames = ["January", "February", "March", "April", "May", "June",
                        "July", "August", "September", "October", "November", "December"];
    const daysInMonth = [31, (isLeapYear(currentYear) ? 29 : 28), 31, 30, 31, 30,
                         31, 31, 30, 31, 30, 31];

    const calendarGrid = document.getElementById('calendarGrid');
    const currentMonthElement = document.getElementById('currentMonth');
    const currentYearElement = document.getElementById('currentYear');
    const eventList = document.getElementById('eventList');

    function isLeapYear(year) {
        return (year % 4 === 0 && (year % 100 !== 0 || year % 400 === 0));
    }

    function updateCalendar() {
        calendarGrid.innerHTML = '';
        const daysInCurrentMonth = daysInMonth[currentMonth];
        currentYearElement.textContent = currentYear;
        currentMonthElement.textContent = monthNames[currentMonth];

        const firstDay = new Date(currentYear, currentMonth, 1).getDay();

        for (let i = 0; i < firstDay; i++) {
            const blankDiv = document.createElement('div');
            blankDiv.classList.add('disabled');
            calendarGrid.appendChild(blankDiv);
        }

        for (let day = 1; day <= daysInCurrentMonth; day++) {
            const dayDiv = document.createElement('div');
            dayDiv.textContent = day;
            dayDiv.classList.add('active');
            calendarGrid.appendChild(dayDiv);
        }

        calendarWithData(calendarData);
    }

    document.getElementById('prevMonth').addEventListener('click', () => {
        currentMonth--;
        if (currentMonth < 0) {
            currentMonth = 11;
            currentYear--;
        }
        updateCalendar();
    });

    document.getElementById('nextMonth').addEventListener('click', () => {
        currentMonth++;
        if (currentMonth > 11) {
            currentMonth = 0;
            currentYear++;
        }
        updateCalendar();
    });

    document.getElementById('prevYear').addEventListener('click', () => {
        currentYear--;
        updateCalendar();
    });

    document.getElementById('nextYear').addEventListener('click', () => {
        currentYear++;
        updateCalendar();
    });

    updateCalendar(); 
    fetchCalendarData();

    async function fetchCalendarData() {
        try {
            const response = await fetch('/api/borick');
            const data = await response.json();
            console.log("Fetched calendar data:", data);
            calendarData = data;
            calendarWithData(calendarData);
        } catch (err) {
            console.error("Failed to load calendar data: ", err);
        }
    }

    function calendarWithData(data) {
        if (!data || data.length === 0) return;
    
        eventsByDay = {};
    
        const weekdayMap = {
            "Sunday": 0,
            "Monday": 1,
            "Tuesday": 2,
            "Wednesday": 3,
            "Thursday": 4,
            "Friday": 5,
            "Saturday": 6
        };
    
        data.forEach(entry => {
            const startDate = new Date(`${entry.Start_Date}T00:00:00`);
            const endDate = new Date(`${entry.End_Date}T00:00:00`);
            const weekdays = entry.Days_Of_the_Week.split(" - ").map(day => weekdayMap[day.trim()]);
    
            if (isNaN(startDate) || isNaN(endDate)) {
                console.warn("Invalid date range:", entry.Start_Date, entry.End_Date);
                return;
            }
    
            const current = new Date(startDate);
    
            while (current <= endDate) {
                const dayOfWeek = current.getDay();
    
                if (weekdays.includes(dayOfWeek)) {
                    const year = current.getFullYear();
                    const month = current.getMonth();
                    const day = current.getDate();
    
                    if (year === currentYear && month === currentMonth) {
                        const key = `${year}-${String(month + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
                        if (!eventsByDay[key]) {
                            eventsByDay[key] = [];
                        }
                        eventsByDay[key].push(entry);
                    }
                }
    
                current.setDate(current.getDate() + 1);
            }
        });
    
        Object.keys(eventsByDay).forEach(key => {
            eventsByDay[key].sort((a, b) => {
                const timeA = extractTime(a.Hours.split(" | ")[1].split(" - ")[0]);
                const timeB = extractTime(b.Hours.split(" | ")[1].split(" - ")[0]);
                return timeA - timeB;
            });
        });
    
        const dayDivs = calendarGrid.querySelectorAll('div.active');
        dayDivs.forEach(div => {
            const day = parseInt(div.textContent);
            const key = `${currentYear}-${String(currentMonth + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
    
            div.classList.remove('event');
            div.onclick = null;
    
            if (eventsByDay[key]) {
                div.classList.add('event');
                div.addEventListener('click', () => {
                    displayEventsForDay(key);
                });
            } else {
                div.addEventListener('click', () => {
                    displayEventsForDay(null);
                });
            }
        });
    }
    
    function extractTime(timeString) {
        const [time, period] = timeString.split(" ");
        const [hours, minutes] = time.split(":").map(num => parseInt(num));
        let totalMinutes = hours * 60 + minutes;
        
        if (period === "PM" && hours !== 12) {
            totalMinutes += 12 * 60;
        } else if (period === "AM" && hours === 12) {
            totalMinutes -= 12 * 60;
        }
        
        return totalMinutes;
    }
    
    function displayEventsForDay(key) {
        eventList.innerHTML = '';
    
        const titleEl = document.getElementById('selectedDayTitle');
    
        if (!key || !eventsByDay[key]) {
            titleEl.textContent = 'No classes on this day:';
            eventList.innerHTML = '<p>No classes on this day.</p>';
            return;
        }
    
        const [year, month, day] = key.split('-');
        const readableDate = `${monthNames[parseInt(month, 10) - 1]} ${parseInt(day, 10)}, ${year}`;
    
        titleEl.textContent = `Classes on ${readableDate}:`;
    
        eventsByDay[key].forEach(event => {
            const div = document.createElement('div');
            div.classList.add('event-entry');
            div.innerHTML = `
                <strong>${event.Title}</strong><br>
                ${event.Instructor}<br>
                ${event.Hours}<br>
                ${event.Locations}
                <hr>
            `;
            eventList.appendChild(div);
        });
    }
});