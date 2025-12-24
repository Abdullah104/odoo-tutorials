import { Component, useState, markup } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";

export class Playground extends Component {
  static template = "awesome_owl.playground";

  static components = { Counter, Card };

  setup() {
    this.state = useState({ sum: 2 });

    this.incrementSum = this.incrementSum.bind(this);
  }

  cardContent = "<div class='text-primary'>some content</div";
  card1Content = this.cardContent;
  card2Content = markup(this.cardContent);

  incrementSum = () => this.state.sum++;
}
