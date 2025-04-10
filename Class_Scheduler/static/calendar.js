document.addEventListener('DOMContentLoaded', function () 
{
    let currentDate = new Date();
    let currentMonth = currentDate.getMonth();
    let currentYear = currentDate.getFullYear();

    const monthNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
    const daysInMonth = [31, (isLeapYear(currentYear) ? 29 : 28), 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];

    const calendarGrid = document.getElementById('calendarGrid');
    const currentMonthElement = document.getElementById('currentMonth');
    const currentYearElement = document.getElementById('currentYear');


    function isLeapYear(year) 
    {
        return (year % 4 === 0 && (year % 100 !== 0 || year % 400 === 0));
    }

    function updateCalendar() 
    {
        calendarGrid.innerHTML = '';
        const daysInCurrentMonth = daysInMonth[currentMonth];
        currentYearElement.textContent = currentYear;
        currentMonthElement.textContent = monthNames[currentMonth];

        for (let day = 1; day <= daysInCurrentMonth; day++) 
        {
            const dayDiv = document.createElement('div');
            dayDiv.textContent = day;
            dayDiv.classList.add('active');
            calendarGrid.appendChild(dayDiv);
        }
    }

    document.getElementById('prevMonth').addEventListener('click', () => 
    {
        currentMonth--;
        if (currentMonth < 0) 
        {
            currentMonth = 11;
            currentYear--;
        }
        updateCalendar();
    });

    document.getElementById('nextMonth').addEventListener('click', () => 
    {
        currentMonth++;
        if (currentMonth > 11) 
        {
            currentMonth = 0;
            currentYear++;
        }
        updateCalendar();
    });

    document.getElementById('prevYear').addEventListener('click', () => 
    {
        currentYear--;
        updateCalendar();
    });

    document.getElementById('nextYear').addEventListener('click', () => 
    {
        currentYear++;
        updateCalendar();
    });

    updateCalendar();
});