'use strict';

const e = React.createElement;

class LikeButton extends React.Component {
  constructor(props) {
    super(props);
    this.state = { liked: false };
  }

  render() {
    if (this.state.liked) {
      return 'Thanks for liking our Music Recommendation Chatbox!!!';
    }

    return e(
      'button',
      { onClick: () => this.setState({ liked: true }) },
      'Please Like Our Chatbox!'
    );
  }
}

const domContainer = document.querySelector('#like_button_container');
ReactDOM.render(e(LikeButton), domContainer);
