window.onload = () => {
  try {
    let colors = getColors();
    if (!colors || colors.length == 0) {
      throw new Error("There are no colors in the database");
    }
    let colorsDiv = document.getElementById("colors");
    let typeColors = [
      {
        type: "bg_color",
        name: "Background Color",
        pair: "text_color",
        pairNumber: 0,
      },
      {
        type: "text_color",
        name: "Text Color",
        pair: "bg_color",
        pairNumber: 1,
      },
      {
        type: "bg_header_color",
        name: "Background Header Color",
        pair: "title_color",
        pairNumber: 0,
      },
      {
        type: "title_color",
        name: "Title Color",
        pair: "bg_header_color",
        pairNumber: 1,
      },
    ];
    if (!colorsDiv) {
      throw new Error("There is no div with id colors");
    }
    colorsDiv.innerHTML = typeColors
      .map((typeColor) => {
        return `<div class="my-3">
        <label for="${typeColor.type}"
        >${typeColor.name}</label>
          <select name="${typeColor.type}" id="${
          typeColor.type
        }" class="form-select bef bef-bg-moccasin bef-text-mystic"
          aria-label="${typeColor.name}">
            <option selected>Select ${typeColor.name}</option>
            ${Object.keys(colors).map((key) => {
              return `<option value="${key}" class="bef bef-bg-${key}">${key}</option>`;
            })}
            <option >None</option>
          </select>
        </div>`;
      })
      .join("");
    typeColors.forEach((typeColor) => {
      let select = document.getElementById(typeColor.type);
      let pairSelect = document.getElementById(typeColor.pair);
      select.addEventListener("change", () => {
        let color = select.value;
        let pairColor = pairSelect.value;
        if (color == "None" || color.includes("Select")) {
          color = "";
        }
        if (pairColor == "None" || pairColor.includes("Select")) {
          pairColor = "";
        }
        console.log(color);
        select.classList = `form-select bef bef-bg-${
          typeColor.pairNumber == 0 && color !== ""
            ? color
            : typeColor.pairNumber === 1 && pairColor !== ""
            ? pairColor
            : "moccasin"
        } bef-text-${
          typeColor.pairNumber === 0 && pairColor !== ""
            ? pairColor
            : typeColor.pairNumber == 1 && color !== ""
            ? color
            : "mystic"
        }`;
        pairSelect.classList = `form-select bef bef-bg-${
          typeColor.pairNumber == 0 && color !== ""
            ? color
            : typeColor.pairNumber === 1 && pairColor !== ""
            ? pairColor
            : "moccasin"
        } bef-text-${
          typeColor.pairNumber === 0 && pairColor !== ""
            ? pairColor
            : typeColor.pairNumber == 1 && color !== ""
            ? color
            : "mystic"
        }`;
        cssCreate();
      });
    });
    /* let selectBGColor = document.getElementById("bg_color");
      let selectTextColor = document.getElementById("text_color");
      let selectBGHeaderColor = document.getElementById("bg_header_color");
      let selectTitleColor = document.getElementById("title_color");
      let BGColor = selectBGColor.value;
      let textColor = selectTextColor.value;
      let BGHeaderColor = selectBGHeaderColor.value;
      let titleColor = selectTitleColor.value;
      selectBGColor.addEventListener("change", () => {
        BGColor = selectBGColor.value;
        if (BGColor == "None") {
          BGColor = "";
        }
        if (BGColor !== "") {
          selectBGColor.classList = `form-select bef bef-bg-${BGColor} bef-text-${textColor}`;
          cssCreate();
        } else {
          selectBGColor.classList = `form-select bef bef-bg-moccasin bef-text-${
            textColor !== "" ? textColor : "mystic"
          }`;
        }
      }); */
    cssCreate();

    let categoryName = document.getElementById("name");
    let submitButton = document.getElementById("submit_button");
    let formMessage = document.getElementById("form_message");
    categoryName.addEventListener("input", function () {
      manageMessageInput();
    });
    categoryName.addEventListener("focusout", function () {
      console.log(categoryName.value.length);
      manageMessageInput();
    });
    function manageMessageInput() {
      if (categoryName.value.length > 3) {
        if (
          formMessage.innerHTML.includes(
            "The name of the category must have more than 3 characters"
          )
        ) {
          formMessage.innerHTML = "";
        }
        submitButton.disabled = false;
      } else {
        formMessage.innerHTML =
          '<p class="text-center text-success">The name of the category must have more than 3 characters</p>';
        submitButton.disabled = true;
      }
    }
    submitButton.addEventListener("click", async () => {
      try {
        let name = categoryName.value;
        if (name.length < 3) {
          throw new Error(
            "The name of the category must have more than 3 characters"
          );
        }
        let BGColor = document.getElementById("bg_color")?.value;
        if (BGColor == "None" || BGColor.includes("Select")) {
          BGColor = "";
        }
        let textColor = document.getElementById("text_color")?.value;
        if (textColor == "None" || textColor.includes("Select")) {
          textColor = "";
        }
        let BGHeaderColor = document.getElementById("bg_header_color")?.value;
        if (BGHeaderColor == "None" || BGHeaderColor.includes("Select")) {
          BGHeaderColor = "";
        }
        let titleColor = document.getElementById("title_color")?.value;
        if (titleColor == "None" || titleColor.includes("Select")) {
          titleColor = "";
        }
        let allClasses = document.getElementById("all_classes")?.value;
        let headerClasses = document.getElementById("header_classes")?.value;
        let boxClasses = document.getElementById("box_classes")?.value;
        let csrftoken = getCookie("csrftoken");
        let response = await fetch(`/todo/create_category`, {
          method: "POST",
          headers: {
            "X-CSRFToken": csrftoken,
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            name: name,
            bg_color: BGColor,
            text_color: textColor,
            bg_header_color: BGHeaderColor,
            title_color: titleColor,
            all_lasses: allClasses,
            header_classes: headerClasses,
            box_classes: boxClasses,
          }),
        });
        console.log(response);
        if (!response.ok) {
          throw new Error("Error al crear la categoría");
        }
        response = await response.json();
        console.log(response);
        if (response.message.includes("Success")) {
          formMessage.innerHTML = `<p class="text-center text-success">${response.message}</p>`;
          setTimeout(() => {
            window.location.href = "/todo/categories";
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
