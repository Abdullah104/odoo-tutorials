import { Component } from "@odoo/owl";
import { TodoModel } from "../todo_model";

export class TodoItem extends Component {
  static template = "awesome_owl.todo_item";

  static props = {
    todo: TodoModel,
    toggleState: Function,
    removeTodo: Function,
  };
}
