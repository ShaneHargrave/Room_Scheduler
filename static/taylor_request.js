function validateForm() {
    const startTime = document.getElementById('startTime').value;
    const endTime = document.getElementById('endTime').value;
    const roomSelect = document.getElementById('roomNumber');
    const selectedRoom = roomSelect.value;
    const submitBtn = document.getElementById('submitBtn');

    const timesValid = startTime && endTime && startTime < endTime;
    const roomValid = selectedRoom && !roomSelect.disabled && selectedRoom !== "No rooms available";

    if (timesValid && roomValid) {
        submitBtn.disabled = false;
    } else {
        submitBtn.disabled = true;
    }
}

document.getElementById('startTime').addEventListener('input', validateForm);
document.getElementById('endTime').addEventListener('input', validateForm);
document.getElementById('roomNumber').addEventListener('change', validateForm);

window.onload = validateForm;