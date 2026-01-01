import { Component, useState, markup } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todo/todo_list/todo_list";

export class Playground extends Component {
  static template = "awesome_owl.playground";

  static components = { Counter, Card, TodoList };

  setup() {
    this.state = useState({ sum: 2 });

    this.incrementSum = this.incrementSum.bind(this);
  }

  cardContent = "<div class='text-primary'>some content</div";
  card1Content = this.cardContent;
  card2Content = markup(this.cardContent);

  incrementSum = () => this.state.sum++;
}
