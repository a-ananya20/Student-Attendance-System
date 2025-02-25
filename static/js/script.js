// Highlight active navigation link
function highlightActiveNav() {
        const currentPath = window.location.pathname;
        const navLinks = document.querySelectorAll('nav ul li a');
        navLinks.forEach(link => {
            if (link.href.includes(currentPath)) {
                link.classList.add('active');
            } else {
                link.classList.remove('active');
            }
        });
    }
    highlightActiveNav();

 // Show/hide sections dynamically (optional feature for dashboard)
function toggleSectionVisibility(sectionId) {
        const section = document.getElementById(sectionId);
        if (section) {
            section.style.display = section.style.display === 'none' ? 'block' : 'none';
        }
    }


/// Toggle all checkboxes when "Select All" is checked
function toggleAll(selectAllCheckbox) {
    // Get all checkboxes in the tbody (excluding the "Select All" checkbox)
    const checkboxes = document.querySelectorAll(".attendance-table tbody input[type='checkbox']");

    // Set each checkbox's checked status to match "Select All"
    checkboxes.forEach((checkbox) => {
        checkbox.checked = selectAllCheckbox.checked;
        updateAttendanceStatus(checkbox);
    });
}

// Update individual attendance status dynamically
function updateAttendance(studentId) {
    const checkbox = document.getElementById(`checkbox_${studentId}`);
    updateAttendanceStatus(checkbox);
}

// Update status label (Present/Absent) dynamically
function updateAttendanceStatus(checkbox) {
    const row = checkbox.closest("tr");

    // Find or create the attendance status cell
    let statusCell = row.querySelector(".attendance-status");
    if (!statusCell) {
        statusCell = document.createElement("td");
        statusCell.classList.add("attendance-status");
        row.appendChild(statusCell);
    }

    // Set status text based on checkbox state
    if (checkbox.checked) {
        statusCell.textContent = "Present";
    } else {
        statusCell.textContent = "Absent";
    }
}

// go back button
function goBack() {
    if (window.history.length > 1) {
        window.history.back();
    } else {
        // Fallback: Redirect to a specific page if no history
        window.location.href = "/";
    }
}

function goDashboard(){
    window.location.href = "{% url 'faculty_dashboard' %}";
}