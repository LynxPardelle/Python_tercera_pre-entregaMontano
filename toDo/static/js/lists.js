window.onload = () => {
  let listName = document.getElementById("list_name");
  let submitButton = document.getElementById("submit_button");
  let listFormMessage = document.getElementById("form_message");
  listName.addEventListener("input", function () {
    manageMessageInput();
  });
  listName.addEventListener("focusout", function () {
    console.log(listName.value.length);
    manageMessageInput();
  });
  function manageMessageInput() {
    if (listName.value.length > 3) {
      if (
        listFormMessage.innerHTML.includes(
          "The name of the list must have more than 3 characters"
        )
      ) {
        listFormMessage.innerHTML = "";
      }
      submitButton.disabled = false;
    } else {
      listFormMessage.innerHTML =
        '<p class="text-center text-success">The name of the list must have more than 3 characters</p>';
      submitButton.disabled = true;
    }
  }
  submitButton.addEventListener("click", async () => {
    try {
      let name = listName.value;
      if (name.length < 3) {
        throw new Error(
          "The name of the list must have more than 3 characters"
        );
      }
      let csrftoken = getCookie("csrftoken");
      let response = await fetch(`/todo/create_list/${name}`, {
        method: "GET",
        headers: {
          "X-CSRFToken": csrftoken,
        },
      });
      if (!response.ok) {
        throw new Error("Error al crear la lista");
      }
      console.log(response);
      response = await response.json();
      console.log(response);
      if (response.message.includes("Success")) {
        listFormMessage.innerHTML = `<p class="text-center text-success">${response.message}</p>`;
        setTimeout(() => {
          window.location.href = "/todo/lists";
        }, 2000);
      } else {
        listFormMessage.innerHTML = `<p class="text-center text-danger">${response.message}</p>`;
      }
    } catch (error) {
      listFormMessage.innerHTML = `<p class="text-center text-danger">${error.message}</p>`;
    }
  });
};
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
