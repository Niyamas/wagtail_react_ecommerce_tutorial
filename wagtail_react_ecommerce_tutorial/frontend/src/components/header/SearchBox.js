import React, { useState } from 'react'
import { Button, Form } from 'react-bootstrap'
import { useHistory } from 'react-router-dom'

import './css/header.css'


function SearchBox(props) {

    // Initialize page-specific state variables
    const [keyword, setKeyword] = useState('')

    // Searchbox is not a page, so we cannot destructure the variables
    // and get history from it. So we use useHistory() instead.
    let history = useHistory()

    const submitHandler = (event) => {
        
        event.preventDefault()

        // If keyword isn't empty, begin search, or go back to home page.
        if (keyword) {

            history.push(`/?keyword=${keyword}&page=1`)
        }
        // If there's no keywords, send the user back to their original page.
        else {

            history.push(history.push(history.location.pathname))
        }

    const getFormClasses = () => {
        
        let classes = props.cname ? props.cname : ''
        classes += "searchbox"
        return classes
    }

    console.log('getFormClasses', getFormClasses)

    }

    return (

        <Form className="searchbox" onSubmit={ submitHandler } inline>
            <Form.Control
                type="text"
                name="q"
                onChange={ (event) => setKeyword(event.target.value) }
                className="searchbox__form mr-sm-2 ml-sm-5"
            >
            </Form.Control>

            <Button
                type="submit"
                variant="outline-success"
                className="p-2"
            >
                Submit
            </Button>
        </Form>

    )
}

export default SearchBox
