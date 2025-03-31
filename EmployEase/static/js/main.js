// JavaScript for enabling drag-and-drop functionality
const dropZone = document.getElementById('fileDropZone');
const fileInput = document.getElementById('policyFile');

// Handle drag over event
dropZone.addEventListener('dragover', function(e) {
    e.preventDefault();
    dropZone.style.backgroundColor = '#eaeaea'; // Change background color on drag over
});

// Handle drop event
dropZone.addEventListener('drop', function(e) {
    e.preventDefault();
    dropZone.style.backgroundColor = '#f7f7f7'; // Reset background color
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        fileInput.files = files; // Set the dropped files to the file input
    }
});

// Trigger file input on click
dropZone.addEventListener('click', function() {
    fileInput.click();
});

document.getElementById("addpolicyForm").addEventListener("submit", function (e) {
    const appraisalDate = document.getElementById("appraisalDate").value;
    if (!appraisalDate) {
        e.preventDefault();
        alert("Please select a valid appraisal date.");
    }
});

// Calculate No of Days and Remaining Days
document.getElementById('toDate').addEventListener('change', function () {
    const fromDate = new Date(document.getElementById('fromDate').value);
    const toDate = new Date(this.value);
    const today = new Date(); // Current date

    if (fromDate && toDate && toDate >= fromDate) {
        // Calculate No of Days
        const differenceInTime = toDate - fromDate;
        const differenceInDays = differenceInTime / (1000 * 3600 * 24) + 1; // Include start date
        document.getElementById('noOfDays').value = differenceInDays;

        // Calculate Remaining Days
        const remainingTime = toDate - today;
        const remainingDays = Math.max(remainingTime / (1000 * 3600 * 24), 0); // Remaining days till "To"
        document.getElementById('remainingDays').value = Math.ceil(remainingDays);
    } else {
        document.getElementById('noOfDays').value = '';
        document.getElementById('remainingDays').value = '';
    }
});

// Filtering birthdays
document.getElementById('month').addEventListener('change', function() {
    this.form.submit();
});

document.getElementById('department').addEventListener('change', function() {
    this.form.submit();
});

// Leave request modal functions
function openModal() {
    document.getElementById('leaveModal').style.display = 'block';
}

function closeModal() {
    document.getElementById('leaveModal').style.display = 'none';
}

function calculateDays() {
    const fromDate = document.getElementById('fromDate').value;
    const toDate = document.getElementById('toDate').value;
    const remainingDaysInput = document.getElementById('remainingDays');
    const noOfDaysInput = document.getElementById('noOfDays');

    if (fromDate && toDate) {
        const startDate = new Date(fromDate);
        const endDate = new Date(toDate);

        if (endDate >= startDate) {
            const differenceInTime = endDate - startDate;
            const differenceInDays = Math.ceil(differenceInTime / (1000 * 60 * 60 * 24)) + 1;

            // Set the calculated number of days
            noOfDaysInput.value = differenceInDays;

            // Example: Assume 20 remaining days initially, adjust after calculation
            const initialRemainingDays = 20;
            const remainingDays = initialRemainingDays - differenceInDays;
            remainingDaysInput.value = remainingDays >= 0 ? remainingDays : 0; // Prevent negative values
        } else {
            alert('The "To" date cannot be earlier than the "From" date.');
            noOfDaysInput.value = '';
            remainingDaysInput.value = '';
        }
    } else {
        noOfDaysInput.value = '';
        remainingDaysInput.value = '';
    }
}
