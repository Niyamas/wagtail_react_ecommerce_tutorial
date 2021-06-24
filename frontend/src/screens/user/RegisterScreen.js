import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { useDispatch, useSelector } from 'react-redux'

import { Form, Button, Row, Col } from 'react-bootstrap'

import Loader from '../../components/shared/Loader'
import Message from '../../components/shared/Message'
import FormContainer from '../../components/shared/FormContainer'

import { register } from '../../actions/userActions'


function RegisterScreen({ location, history }) {

    // State variables.
    const [name, setName] = useState('')
    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')
    const [confirmPassword, setConfirmPassword] = useState('')
    const [message, setMessage] = useState('')

    // A redux hook that dispatches an action. Like setState, but redux
    // dispatch is used to trigger an action
    const dispatch = useDispatch()

    // Get the querystring in the URL parameters and store its value in redirect if possible.
    const redirect = location.search ? location.search.split('=')[1] : '/'

    // Get userRegister variables from the state.
    const userRegister = useSelector( (state) => state.userRegister )
    const { loading, userInfo, error } = userRegister

    // Trigger state change when history, userInfo, or redirect changes.
    useEffect( () => {

        // If the user is logged in, redirect the user to 
        if (userInfo) {

            history.push(redirect)
        }
    }, [history, userInfo, redirect])

    // Handles when the user clicks the "Sign In" button.
    const submitHandler = (event) => {

        // Prevents the form from being submitted.
        event.preventDefault()

        // Show a custom error if the password is not equal to the confirmed password field.
        // If they do, dispatch the register action.
        if (password !== confirmPassword) {

            setMessage('Passwords do not match.')
        }
        else {

            // Call the regsiter action -> reducer -> update state
            dispatch( register(name, email, password) )
        }

    }

    return (

        <FormContainer>
            <h1>Register</h1>

            {/* This error shows when the passwords don't match */}
            { message && <Message variant="danger">{ message }</Message> }

            {/* This error shows when something like an email already exists for that username. */}
            { error && <Message variant="danger">{ error }</Message> }

            { loading && <Loader /> }

            <Form onSubmit={ submitHandler }>
                <Form.Group controlId="name" className="register__form">
                    <Form.Label>Name</Form.Label>
                    <Form.Control
                        type="name"
                        placeholder="Name"
                        value={name}
                        onChange={ (event) => setName(event.target.value) }
                        required
                    >
                    </Form.Control>
                </Form.Group>

                <Form.Group controlId="email" className="register__form">
                    <Form.Label>Email Address</Form.Label>
                    <Form.Control
                        type="email"
                        placeholder="Email"
                        value={email}
                        onChange={ (event) => setEmail(event.target.value) }
                        required
                    >
                    </Form.Control>
                </Form.Group>

                <Form.Group controlId="password" className="register__form">
                    <Form.Label>Password</Form.Label>
                    <Form.Control
                        type="password"
                        placeholder="Password"
                        value={password}
                        onChange={ (event) => setPassword(event.target.value) }
                        required
                    >
                    </Form.Control>
                </Form.Group>

                <Form.Group controlId="passwordConfirm" className="register__form">
                    <Form.Label>Confirm Password</Form.Label>
                    <Form.Control
                        type="password"
                        placeholder="Confirm Password"
                        value={confirmPassword}
                        onChange={ (event) => setConfirmPassword(event.target.value) }
                        required
                    >
                    </Form.Control>
                </Form.Group>

                <Button className="btn-conglomerate register-btn" type="submit" variant="primary">Register</Button>
            </Form>

            <Row className="py-3">
                <Col>
                    Have an Account?&nbsp;
                    <Link
                        /* Check if redirect is there, if not, go to the register page. */
                        to={ redirect ? `/login?redirect=${ redirect }` : '/login' }
                    >
                        Sign In
                    </Link>
                </Col>
            </Row>

        </FormContainer>

    )
}

export default RegisterScreen
