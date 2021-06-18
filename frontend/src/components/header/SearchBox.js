import React, { useState } from 'react'
import { Button, Form } from 'react-bootstrap'
import { useHistory } from 'react-router-dom'


function SearchBox() {

    // Initialize page-specific state variables
    const [keyword, setKeyword] = useState('')

    let history = useHistory()

    const submitHandler = (event) => {
        
        event.preventDefault()

        // If keyword isn't empty, begin search, or go back to home page.
        if (keyword) {

            history.push(`/?keyword=${keyword}`)
        }
        // If there's no keywords, send the user back to their original page.
        else {

            history.push(history.push(history.location.pathname))
        }

        //
    }

    return (

        <Form onSubmit={ submitHandler } inline>
            <Form.Control
                type="text"
                name="q"
                onChange={ (event) => setKeyword(event.target.value) }
                className="mr-sm-2 ml-sm-5"
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
