document.addEventListener("DOMContentLoaded", () => {
    // Add student
    document.getElementById('create-student-form')?.addEventListener('submit', async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post(`${API_URL}/students/`, {
                name: document.getElementById('name').value,
                email: document.getElementById('email').value,
                seniority: document.getElementById('seniority').value
            }, 
            {
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            alert('Student added successfully!');
            e.target.reset();
        } catch (error) {
            alert('Error adding student: ' + error.response?.data?.message || error.message);
        }
    });
});

// list students

function fetchStudents() {
    axios.get(`${API_URL}/students/`) 
        .then(response => {
            const students = response.data;
            const tableBody = document.querySelector("#students-table tbody");

            // Clear the table body before adding new rows
            tableBody.innerHTML = '';

            // Loop through the students data and create table rows
            students.forEach(student => {
                const row = document.createElement("tr");

                // Create table cells for each student's attribute
                const nameCell = document.createElement("td");
                nameCell.textContent = student.name;
                row.appendChild(nameCell);

                const emailCell = document.createElement("td");
                emailCell.textContent = student.email;
                row.appendChild(emailCell);

                const seniorityCell = document.createElement("td");
                seniorityCell.textContent = student.seniority;
                row.appendChild(seniorityCell);

                // Append the row to the table body
                tableBody.appendChild(row);
            });
        })
        .catch(error => {
            console.error("Error fetching students:", error);
        });
}


// call the funtion to log ab test event
function logListStudentsViewedAB() {
    axios.post(`${API_URL}/abtest/`, {
        event_type: "list_students_viewed",
        variant: `${VARIANT}`,
        session_id: `${SESSION_ID}`,

    })
    .catch(error => {
        console.error("Error logging AB test event:", error);
    });
}