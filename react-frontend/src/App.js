import React, {Component} from 'react';
import './App.css';
import Search from './components/Search';
import 'bootstrap/dist/css/bootstrap.min.css';
import logoimg from './btimg.png';

class App extends Component {
  render() {
    return (
      <div className="App">
        <img style={{ width: '10%', marginTop: 25}} src = {logoimg} />
        <Search />
      </div>
    )
  }
}

export default App;
