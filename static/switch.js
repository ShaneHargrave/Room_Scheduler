function showTab(tab) {
    const classesTab = document.getElementById("classesTab");
    const eventsTab = document.getElementById("eventsTab");
    const classesSection = document.getElementById("classesSection");
    const eventsSection = document.getElementById("eventsSection");

    if (tab === 'classes') {
        classesSection.style.display = 'block';
        eventsSection.style.display = 'none';
        classesTab.classList.add('active');
        eventsTab.classList.remove('active');
    } else if (tab === 'events') {
        classesSection.style.display = 'none';
        eventsSection.style.display = 'block';
        eventsTab.classList.add('active');
        classesTab.classList.remove('active');
    }
}