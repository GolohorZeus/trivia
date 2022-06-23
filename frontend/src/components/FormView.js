import React, { Component } from "react";
import $ from "jquery";
import "../stylesheets/FormView.css";

class FormView extends Component {
  constructor(props) {
    super();
    this.state = {
      question: "",
      answer: "",
      difficulty: 1,
      rating: 1,
      category: 1,
      categories: {},
      newCategory: "",
    };
  }

  componentDidMount() {
    $.ajax({
      url: `/categories`, //TODO: update request URL
      type: "GET",
      success: (result) => {
        this.setState({ categories: result.categories });
        return;
      },
      error: (error) => {
        alert("Unable to load categories. Please try your request again");
        return;
      },
    });
  }

  submitCategory = (event) => {
    // prevent default behaviour
    event.preventDefault();
    $.ajax({
      url: "/categories",
      type: "POST",
      contentType: "application/json",
      data: JSON.stringify({
        newCategory: this.state.newCategory,
      }),
      xhrFields: {
        withCredentials: true,
      },
      crossDomain: true,
      success: (result) => {
        alert(`New category ${this.state.newCategory} added.`);
        return;
      },
      error: (error) => {
        alert("Unable to add category. Please try your request again");
        return;
      },
    });
  };

  submitQuestion = (event) => {
    event.preventDefault();
    $.ajax({
      url: "/questions", //TODO: update request URL
      type: "POST",
      dataType: "json",
      contentType: "application/json",
      data: JSON.stringify({
        question: this.state.question,
        answer: this.state.answer,
        difficulty: this.state.difficulty,
        rating: this.state.rating,
        category: this.state.category,
      }),
      xhrFields: {
        withCredentials: true,
      },
      crossDomain: true,
      success: (result) => {
        document.getElementById("add-question-form").reset();
        return;
      },
      error: (error) => {
        alert("Unable to add question. Please try your request again");
        return;
      },
    });
  };

  handleChange = (event) => {
    this.setState({ [event.target.name]: event.target.value });
  };

  render() {
    return (
      <div id="add-form">
        <h2>Add a New Trivia Question</h2>
        <form
          className="form-view"
          id="add-question-form"
          onSubmit={this.submitQuestion}
        >
          <label>
            Question
            <input
              type="text"
              name="question"
              onChange={this.handleChange}
              required
            />
          </label>
          <label>
            Answer
            <input
              type="text"
              name="answer"
              onChange={this.handleChange}
              required
            />
          </label>
          <label>
            Difficulty
            <select name="difficulty" onChange={this.handleChange} required>
              <option value="1">1</option>
              <option value="2">2</option>
              <option value="3">3</option>
              <option value="4">4</option>
              <option value="5">5</option>
            </select>
          </label>
          <label>
            Rating
            <select name="rating" onChange={this.handleChange} required>
              <option value="1">1</option>
              <option value="2">2</option>
              <option value="3">3</option>
              <option value="4">4</option>
              <option value="5">5</option>
            </select>
          </label>
          <label>
            Category
            <select name="category" onChange={this.handleChange}>
              {Object.keys(this.state.categories).map((id) => {
                return (
                  <option key={id} value={id}>
                    {this.state.categories[id]}
                  </option>
                );
              })}
            </select>
          </label>
          <input type="submit" className="button" value="Submit" />
        </form>
        <h2>Add a New Trivia Category</h2>
        <form
          className="form-view"
          id="add-category-form"
          onSubmit={this.submitCategory}
        >
          <label>
            Category
            <input
              type="text"
              name="newCategory"
              onChange={this.handleChange}
              required
            />
          </label>
          <input type="submit" className="button" value="Submit" />
        </form>
      </div>
    );
  }
}

export default FormView;
