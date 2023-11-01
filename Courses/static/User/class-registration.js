function submitButton() {
  let registrationForm = document.getElementById("registrationForm");
  let submitBtn = document.getElementById("submit");

  submitBtn.addEventListener("click", () => {
    if (confirm("Do you want to submit?")) {
      registrationForm.submit();
    } else {
      return false;
    }
  })
}

function searchSubject() {
  let filter;
  let searchInput = document.getElementById("search");
  let classTable = document.getElementById("class-table");
  let classRows = classTable.tBodies[0].rows;

  searchInput.addEventListener("keyup", () => {
    filter = searchInput.value.toUpperCase();
    for (const classRowElement of classRows) {
      let subjectName = classRowElement.cells[1].innerText;
      if (subjectName.toUpperCase().indexOf(filter) > -1) {
        classRowElement.style.display = null;
      } else {
        classRowElement.style.display = "none";
      }
    }
  })
}

searchSubject();
submitButton();
