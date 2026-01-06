import { Component, useState, useRef, onMounted } from "@odoo/owl";
import { TodoItem } from "../todo_item/todo_item";
import { TodoModel } from "../todo_model";
import { useAutoFocus } from "../../utils";

export class TodoList extends Component {
  static template = "awesome_owl.todo_list";

  static components = { TodoItem };

  idCounter = 1;

  setup() {
    this.todos = useState([]);
    this.inputRef = useRef("input");

    onMounted(() => useAutoFocus(this.inputRef))
  }

  addTodo(event) {
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
  }
}
