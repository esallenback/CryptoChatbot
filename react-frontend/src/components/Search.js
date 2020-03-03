import React, { Component } from 'react'
import Button from 'react-bootstrap/Button';

class Search extends Component {

    constructor(props) {
        super(props)
    
        this.state = {
             usersearch:''
        }
    }

    handleSearchChange = (event) => {
        this.setState({
            usersearch: event.target.value
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
                <Button style={{marginTop: 10}} type="submit" size="lg"> Search </Button>
            </form>
        )
    }
}

export default Search
