import React, { useState, useEffect } from 'react'
import { useDispatch, useSelector } from 'react-redux'

import { Form, Button, Row, Col, Table } from 'react-bootstrap'
import { LinkContainer } from 'react-router-bootstrap'

import Loader from '../../components/shared/Loader'
import Message from '../../components/shared/Message'

import { getUserDetails, updateUserProfile } from '../../actions/userActions'
import { listMyOrders } from '../../actions/orderActions'

import { USER_UPDATE_PROFILE_RESET } from '../../constants/userConstants'

import './css/user.css'


function ProfileScreen({ history }) {

    // State variables.
    const [name, setName] = useState('')
    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')
    const [confirmPassword, setConfirmPassword] = useState('')
    const [message, setMessage] = useState('')

    // A redux hook that dispatches an action. Like setState, but redux
    // dispatch is used to trigger an action
    const dispatch = useDispatch()

    // Get userDetails variables from the state.
    const userDetails = useSelector( (state) => state.userDetails )
    const { loading, user, error } = userDetails

    // Get userLogin variable from the state.
    const userLogin = useSelector( (state) => state.userLogin )
    const { userInfo } = userLogin

    // Get userUpdateProfile variable from the state.
    // The success variable, when set to true, will call an action to reset the state.
    const userUpdateProfile = useSelector( (state) => state.userUpdateProfile )
    const { success } = userUpdateProfile

    // Get nested state variables within the parent orderListMy state variable.
    const orderListMy = useSelector( (state) => state.orderListMy )
    const { loading:loadingOrders, error:errorOrders, orders } = orderListMy

    // Trigger state change when history, userInfo, or redirect changes.
    useEffect( () => {

        // If the user isn't logged in, redirect user to the login page.
        // If the user is logged in, 
        if (!userInfo) {

            history.push('/login')
        }
        else {

            // Check if the user data is loaded. If not, get it.
            // Also checks if the user has just updated their profile (success=true).
            if ( !user || !user.first_name || success ) {

                // Resets the profile
                dispatch({ type: USER_UPDATE_PROFILE_RESET })

                // idOrPage is part of URL: /api/v1/users/${idOrPage}/, which is 'profile'.
                dispatch(getUserDetails('profile'))
            }
            else {

                // Update state with user's name and email.
                setName(user.first_name + ' ' + user.last_name)
                setEmail(user.email)
            }

            // Dispatch action to pull from the API a list of the customer's carts and orders.
            dispatch(listMyOrders())
        }
    }, [dispatch, history, user, userInfo, success])

    // Handles when the user clicks the "Sign In" button.
    const submitHandler = (event) => {

        // Prevents the form from being submitted.
        event.preventDefault()

        // Password validation
        // Show a custom error if the password is not equal to the confirmed password field.
        // If they do, dispatch the register action.
        if (password !== confirmPassword) {

            setMessage('Passwords do not match.')
        }
        else if (password.length < 7 || confirmPassword < 7) {

            setMessage('Please use a password with more than 7 characters.')
        }
        else {

            // Call the update user profile action -> reducer -> update state
            dispatch(updateUserProfile({
                'id': user.id,
                'name': name,
                'email': email,
                'password': password
            }))

            // Clear any previous messages.
            setMessage('')
        }
    }

    return (

        <Row>
            <Col className="profile" md={3}>
                <h2>User Profile</h2>

                {/* This error shows when the passwords don't match */}
                { message && <Message variant="danger">{ message }</Message> }

                {/* This error shows when something like an email already exists for that username. */}
                { error && <Message variant="danger">{ error }</Message> }

                { loading && <Loader /> }

                <Form onSubmit={ submitHandler }>
                    <Form.Group controlId="name" className="profile__form">
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

                    <Form.Group controlId="email" className="profile__form">
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

                    <Form.Group controlId="password" className="profile__form">
                        <Form.Label>Password</Form.Label>
                        <Form.Control
                            type="password"
                            placeholder="Password"
                            value={password}
                            onChange={ (event) => setPassword(event.target.value) }
                        >
                        </Form.Control>
                    </Form.Group>

                    <Form.Group controlId="passwordConfirm" className="profile__form">
                        <Form.Label>Confirm Password</Form.Label>
                        <Form.Control
                            type="password"
                            placeholder="Confirm Password"
                            value={confirmPassword}
                            onChange={ (event) => setConfirmPassword(event.target.value) }
                        >
                        </Form.Control>
                    </Form.Group>

                    <Button className="btn-conglomerate profile-update-btn" type="submit" variant="primary">Update</Button>
                </Form>
            </Col>

            <Col md={7}>
                <h2>My Orders</h2>
                {
                    loadingOrders ? (
                        <Loader />
                    ) : (
                        errorOrders ? (
                            <Message variant="danger">{errorOrders}</Message>
                        ) : (
                            <Table striped responsive className="table-sm">
                                <thead>
                                    <tr>
                                        <th>ID</th>
                                        <th>Date</th>
                                        <th>Total</th>
                                        <th>Payed</th>
                                        <th>Delivered</th>
                                        <th></th>
                                    </tr>
                                </thead>

                                <tbody>
                                    {
                                        orders.map( (order) => (
                                            <tr key={order.id}>
                                                <td>{order.id}</td>
                                                <td>{order.created_at.substring(0, 10)}</td>
                                                <td>${order.total_price}</td>
                                                <td>
                                                    {
                                                        order.is_paid ? order.paid_at.substring(0, 10) : (
                                                            <i className="fas fa-times" style={{ color: 'red' }}></i>
                                                        )
                                                    }
                                                </td>
                                                <td>
                                                    <LinkContainer to= {`/order/${order.id}`}>
                                                        <Button className="btn-conglomerate btn-sm">Details</Button>
                                                    </LinkContainer>
                                                </td>
                                            </tr>
                                        ))
                                    }
                                </tbody>
                            </Table>
                        )
                    )
                }
            </Col>
        </Row>

    )
}

export default ProfileScreen
