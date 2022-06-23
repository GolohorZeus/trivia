import React, { Component } from "react";
import "../stylesheets/App.css";
import Question from "./Question";
import Search from "./Search";
import $ from "jquery";

class QuestionView extends Component {
  constructor() {
    super();
    this.state = {
      questions: [],
      page: 1,
      totalQuestions: 0,
      categories: {},
      currentCategory: null,
    };
  }

  componentDidMount() {
    // this.getQuestions();
    this.pageNumberSetUp();
  }

  pageNumberSetUp = () => {
    // to get question page number
    const questionPage = window.location.href.split("/")[3]
      ? window.location.href.split("/")[3]
      : null;
    // to check if the page is set via the url if not set page default to 1
    if (questionPage === null) {
      // this.setState({ page: 1 });
      this.selectPage(1);
    } else {
      // to check if question url is true
      const que = questionPage.split("?")[0];
      if (que === "questions") {
        // to check if page and page number is set
        const pageNNumber = questionPage.split("?")[1].split("=");
        // to check if page query exist
        if (pageNNumber[0] === "page") {
          this.selectPage(Number(pageNNumber[1]));
        }
      }
    }
  };

  getQuestions = () => {
    $.ajax({
      url: `/questions?page=${this.state.page}`, //TODO: update request URL
      type: "GET",
      success: (result) => {
        this.setState({
          questions: result.questions,
          totalQuestions: result.total_questions,
          categories: result.categories,
          currentCategory: result.current_category,
        });
        return;
      },
      error: (error) => {
        // alert("Unable to load questions. Please try your request again");
        // return;
        // if there is an error give the user an option to return to the homepage
        if (
          window.confirm(
            "Unable to load questions. Please try your request again or click ok to visit the homepage"
          )
        ) {
          // homepage route
          window.location.href = "/";
        }
      },
    });
  };

  selectPage(num) {
    this.setState({ page: num }, () => this.getQuestions());
  }

  // Addittional feature
  // to make sure that the always start at the top
  pageScrollTO(xCoord = 0, yCoord = 0) {
    // xCoord is the pixel along the horizontal axis.
    // yCoord is the pixel along the vertical axis.
    window.scrollTo(xCoord, yCoord);
  }

  createPagination() {
    // Addittional feature
    // scroll to the top of a page
    this.pageScrollTO(0, 0);
    let pageNumbers = [];
    let maxPage = Math.ceil(this.state.totalQuestions / 10);
    for (let i = 1; i <= maxPage; i++) {
      pageNumbers.push(
        <span
          key={i}
          className={`page-num ${i === this.state.page ? "active" : ""}`}
          onClick={() => {
            this.selectPage(i);
          }}
        >
          {i}
        </span>
      );
    }
    return pageNumbers;
  }

  getByCategory = (id) => {
    $.ajax({
      url: `/categories/${id}/questions`, //TODO: update request URL
      type: "GET",
      success: (result) => {
        this.setState({
          questions: result.questions,
          totalQuestions: result.total_questions,
          currentCategory: result.current_category,
        });
        return;
      },
      error: (error) => {
        alert("Unable to load questions. Please try your request again");
        return;
      },
    });
  };

  submitSearch = (searchTerm) => {
    $.ajax({
      url: `/questions`, //TODO: update request URL
      type: "POST",
      dataType: "json",
      contentType: "application/json",
      data: JSON.stringify({ searchTerm: searchTerm }),
      xhrFields: {
        withCredentials: true,
      },
      crossDomain: true,
      success: (result) => {
        this.setState({
          questions: result.questions,
          totalQuestions: result.total_questions,
          currentCategory: result.current_category,
        });
        return;
      },
      error: (error) => {
        alert("Unable to load questions. Please try your request again");
        return;
      },
    });
  };

  questionAction = (id) => (action) => {
    if (action === "DELETE") {
      if (window.confirm("are you sure you want to delete the question?")) {
        $.ajax({
          url: `/questions/${id}`, //TODO: update request URL
          type: "DELETE",
          success: (result) => {
            // to store the delete question id
            const questionId = result.deleted_question;
            // to store the question index from the state
            const questionIndex = this.state.questions
              .map((o) => o.id)
              .indexOf(Number(questionId));
            // to check if a valid index is stored
            if (questionIndex !== -1) {
              // deleting the question from the state
              this.state.questions.splice(questionIndex, 1);
              // updating the state
              this.setState(this.state);
            }
          },
          error: (error) => {
            alert("Unable to load questions. Please try your request again");
            return;
          },
        });
      }
    }
  };

  checkIfImageExists = (imageName = null, id) => {
    // // getting the element from the DOM
    const getCat2 = document.querySelector(`#category_id_` + id);
    // to make sure the image loads only once
    if (getCat2 == null) {
      // to check image name not null
      if (imageName !== null) {
        // to check image exists
        $.ajax({
          url: window.location.href + imageName + `.svg`,
          type: "GET",
          success: (result) => {
            const getCat = document.querySelector(`#category_id_` + id);
            // to check if the images have been loaded before if not load it
            if (getCat.dataset.cat_img_loaded === "false") {
              // creating image element
              const image = document.createElement("img");
              // adding some details to the image
              image.setAttribute("src", imageName.toLowerCase() + `.svg`);
              image.setAttribute("alt", imageName.toLowerCase());
              image.setAttribute("class", "category");
              // to confirm the image was successfully loaded
              // image.onload = function handleImageLoaded() {
              //   console.log("image loaded successfully");
              // };
              getCat.appendChild(image);
              // setting the category image loaded to truee after loading the image
              getCat.dataset.cat_img_loaded = true;
            }
          },
          error: (error) => {
            console.error(
              "The new category" +
                " '" +
                imageName +
                "' " +
                "does not have an image the science image would be used as a default image for such categories."
            );
            const getCat = document.querySelector(`#category_id_` + id);
            // to check if the images have been loaded before if not load it
            if (getCat.dataset.cat_img_loaded === "false") {
              // creating image element
              const image = document.createElement("img");
              // adding some details to the image
              image.setAttribute("src", `science.svg`);
              image.setAttribute("alt", imageName.toLowerCase());
              image.setAttribute("class", "category");
              // to confirm the image was successfully loaded
              // image.onload = function handleImageLoaded() {
              //   console.log("image loaded successfully");
              // };
              getCat.appendChild(image);
              // setting the category image loaded to truee after loading the image
              getCat.dataset.cat_img_loaded = true;
            }
          },
        });
      }
    }
  };

  render() {
    return (
      <div className="question-view">
        <div className="categories-list">
          <h2
            onClick={() => {
              this.getQuestions();
            }}
          >
            Categories
          </h2>
          <ul>
            {Object.keys(this.state.categories).map((id) => (
              <li
                key={id}
                onClick={() => {
                  this.getByCategory(id);
                }}
                id={`category_id_` + id}
                data-cat_img_loaded={false}
              >
                {this.state.categories[id]}
                {this.checkIfImageExists(this.state.categories[id], id)}
              </li>
            ))}
          </ul>
          <Search submitSearch={this.submitSearch} />
        </div>
        <div className="questions-list">
          <h2>Questions</h2>
          {this.state.questions.map((q, ind) => (
            <Question
              key={q.id}
              question_id={q.id}
              rating={q.rating}
              question={q.question}
              answer={q.answer}
              category={this.state.categories[q.category]}
              difficulty={q.difficulty}
              questionAction={this.questionAction(q.id)}
            />
          ))}
          <div className="pagination-menu">{this.createPagination()}</div>
        </div>
      </div>
    );
  }
}

export default QuestionView;
