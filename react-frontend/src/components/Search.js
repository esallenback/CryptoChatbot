import React, { Component } from 'react'
import Button from 'react-bootstrap/Button';

class Search extends Component {

    constructor(props) {
        super(props)
    
        this.state = {
             usersearch: '',
             history: []
        }
    }

    handleSearchChange = (event) => {
        let search = event.target.value;
        let result = "The user searched for " + search;
        this.setState({
            usersearch: search,
            history: this.state.history.concat([search, result]),
        })
    }

    handleSubmit = (event) => {
        alert(`The user has searched for: ${this.state.usersearch}`)
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
            let itemClass = index % 2 == 0 ? 'search-entry' : 'result-entry';
            historyElements.push(
                <p key={index} class={itemClass}>
                    { value }
                </p>
            );
        }

        return (
            <div class="history">
                {historyElements}
            </div>
        )
    }
    
    render() {
        return (
            <form onSubmit = {this.handleSubmit}>
                <div >
                    <input style={{ width: '60%', marginTop: 25}}
                        type = 'text' 
                        placeholder = "Search for your favorite crypto..."
                        value = {this.state.usersearch}
                        onChange = {this.handleSearchChange}
                    />
                    <button type="reset" onClick = {this.clearSearch}>x</button>
                </div>
                {this.renderHistory()}
                <Button style={{marginTop: 10}} type="submit" size="lg"> Search </Button>
            </form>
        )
    }
}

export default Search
