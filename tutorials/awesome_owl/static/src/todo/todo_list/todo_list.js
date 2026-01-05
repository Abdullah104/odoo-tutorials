import { Component, useState, useRef } from "@odoo/owl";
import { TodoItem } from "../todo_item/todo_item";
import { TodoModel } from "../todo_model";

export class TodoList extends Component {
  static template = "awesome_owl.todo_list";

  static components = { TodoItem };

  idCounter = 1;

  setup() {
    this.todos = useState([]);
    this.inputRef = useRef("input");
  }

  addTodo = (event) => {
    if (event.keyCode !== 13) return;

    if (!event.target.value) return;

    this.todos.push(
      new TodoModel({
        id: this.idCounter++,
        description: event.target.value,
        isCompleted: false,
      })
    );

    event.target.value = "";
  };
}
