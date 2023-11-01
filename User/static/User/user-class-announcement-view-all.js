function searchSubject() {
  let filter;
  let searchInput = document.getElementById("search");
  let articles = document.querySelectorAll("article.courses-announcements > article.searchable");

  searchInput.addEventListener("keyup", () => {
    filter = searchInput.value.toUpperCase();
    for (const article of articles) {
      let subjectName = article.querySelector("a.heading > h3").innerText;
      if (subjectName.toUpperCase().indexOf(filter) > -1) {
        article.style.display = null;
      } else {
        article.style.display = "none";
      }
    }
  })
}

searchSubject();
