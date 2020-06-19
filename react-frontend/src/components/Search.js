import React, { Component } from 'react'
import Button from 'react-bootstrap/Button';
import './Search.css';

class Search extends Component {

    constructor(props) {
        super(props)
    
        this.state = {
             usersearch: '',
             history: []
        }
    }

    handleSearchChange = (event) => {
        this.setState({
            usersearch: event.target.value,
        })
    }

    handleSubmit = (event) => {
        let search = this.state.usersearch;
        let result = "The user searched for " + search;
        this.setState({
            history: this.state.history.concat([search, result]),
            usersearch: ''
        });
        event.preventDefault()
    }

    clearSearch = () => {
        this.setState({
            usersearch: ""
        })
    }

    renderHistory() {
        let historyElements = [];
        for (const [index, value] of this.state.history.entries()) {
            let itemClass = index % 2 === 0 ? 'search-entry' : 'result-entry';
            historyElements.push(
                <p key={index} className={itemClass}>
                    { value }
                </p>
            );
        }

        return (
            <div className="history">
                {historyElements}
            </div>
        )
    }
    
    render() {
        return (
            <div className="container">
                <form onSubmit = {this.handleSubmit} id="search-form">
                        <input id="search-input"
                            type = 'text' 
                            placeholder = "Search for your favorite crypto..."
                            value = {this.state.usersearch}
                            onChange = {this.handleSearchChange}
                        />
                        <button type="reset" onClick = {this.clearSearch}>x</button>
                    <Button style={{marginTop: 10}} type="submit" size="lg"> Search </Button>
                </form>
                {this.renderHistory()}
            </div>
        )
    }
}

export default Search
