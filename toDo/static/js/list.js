window.onload = async () => {
  try {
    let categories = await fetch("/todo/get_categories");
    if (!categories.ok) {
      throw new Error("Error al cargar las categorías");
    }
    categories = await categories.json();
    console.log(categories);
    let categoriesDiv = document.getElementById("categories");
    if (!categoriesDiv) {
      throw new Error("Error al cargar las categorías");
    }
    categoriesDiv.innerHTML = `<div class="my-3">
        <label for="category"
        >Category</label>
          <select name="category" id="category" class="form-select bef bef-bg-moccasin bef-text-mystic"
          aria-label="Category">
            ${categories.data.map((category) => {
              return `<option value="${category.id}" class="bef bef-bg-${category.bg_color} bef-text-${category.text_color}">${category.name}</option>`;
            })}
          </select>
        </div>`;
    let select = document.getElementById("category");
    select.addEventListener("change", () => {
      let bg_color = select.value
        ? categories.data.find((category) => category.id == select.value)
            .bg_color
        : "";
      let text_color = select.value
        ? categories.data.find((category) => category.id == select.value)
            .text_color
        : "";
      select.classList = `form-select bef bef-bg-${bg_color} bef-text-${text_color}`;
    });
    cssCreate();
    let toDoTitle = document.getElementById("title");
    let submitButton = document.getElementById("submit_button");
    let formMessage = document.getElementById("form_message");
    toDoTitle.addEventListener("input", function () {
      manageMessageInput();
    });
    toDoTitle.addEventListener("focusout", function () {
      console.log(toDoTitle.value.length);
      manageMessageInput();
    });
    function manageMessageInput() {
      if (toDoTitle.value.length > 3) {
        if (
          formMessage.innerHTML.includes(
            "The title of the toDo must have more than 3 characters"
          )
        ) {
          formMessage.innerHTML = "";
        }
        submitButton.disabled = false;
      } else {
        formMessage.innerHTML =
          '<p class="text-center text-success">The title of the toDo must have more than 3 characters</p>';
        submitButton.disabled = true;
      }
    }
    submitButton.addEventListener("click", async () => {
      try {
        let title = toDoTitle.value;
        if (title.length < 3) {
          throw new Error(
            "The title of the toDo must have more than 3 characters"
          );
        }
        let description = document.getElementById("description")?.value;
        let priority = document.getElementById("priority")?.value;
        let completed = !!document.getElementById("completed")?.checked;
        let category = document.getElementById("category")?.value;
        if (category == "None" || category.includes("Select")) {
          category = "";
        }
        if (category == "") {
          throw new Error("You must select a category");
        }
        let csrftoken = getCookie("csrftoken");
        let idDiv = document.getElementById("list_id");
        if (!idDiv) {
          throw new Error("Error creating the toDo, there is no id");
        }
        console.log(idDiv);
        console.log(idDiv.innerHTML);
        let id = idDiv.innerHTML;
        if (!id) {
          throw new Error("Error creating the toDo, there is no id");
        }
        console.log(category);
        console.log(id);
        let response = await fetch(`/todo/create_todo/${category}/${id}`, {
          method: "POST",
          headers: {
            "X-CSRFToken": csrftoken,
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            title: title,
            description: description,
            priority: priority,
            completed: completed,
          }),
        });
        console.log(response);
        if (!response.ok) {
          throw new Error("Error creating the toDo");
        }
        response = await response.json();
        console.log(response);
        if (response.message.includes("Success")) {
          formMessage.innerHTML = `<p class="text-center text-success">${response.message}</p>`;
          setTimeout(() => {
            window.location.href = `/todo/list/${id}`;
          }, 2000);
        } else {
          formMessage.innerHTML = `<p class="text-center text-danger">${response.message}</p>`;
        }
      } catch (error) {
        formMessage.innerHTML = `<p class="text-center text-danger">${error.message}</p>`;
      }
    });
    function getCookie(name) {
      let cookieValue = null;
      if (document.cookie && document.cookie !== "") {
        let cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
          let cookie = cookies[i].trim();
          if (cookie.substring(0, name.length + 1) === name + "=") {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
          }
        }
      }
      console.log(cookieValue);
      return cookieValue;
    }
  } catch (error) {
    console.error(error);
  }
};
