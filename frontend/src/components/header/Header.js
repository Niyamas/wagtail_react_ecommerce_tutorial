import React from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { Navbar, Nav, NavDropdown, Container } from 'react-bootstrap'
import { LinkContainer } from 'react-router-bootstrap'

import SearchBox from './SearchBox'

import { logout } from '../../actions/userActions'      // Actions -> Reducers -> Change state

import './css/header.css'

function Header() {

    // Grab from the state the userInfo
    const userLogin = useSelector( (state) => state.userLogin )
    const { userInfo } = userLogin

    // A redux hook that dispatches an action. Like setState, but redux
    // dispatch is used to trigger an action
    const dispatch = useDispatch()

    // Logs the user out when he/she clicks the login button from the header.
    const logoutHandler = () => {

        // Dispatch the logout action, which then connects to the reducer, and finally the state update.
        dispatch( logout() )
    }

    return (

        <header>
            <Navbar bg="dark" variant="dark" expand="lg" collapseOnSelect>
                <Container>

                    <LinkContainer to='/'>
                        <Navbar.Brand href="/">Brickshop Emporium</Navbar.Brand>
                    </LinkContainer>
                    
                    <Navbar.Toggle aria-controls="basic-navbar-nav" />

                    <Navbar.Collapse id="basic-navbar-nav" className="navbar__right">
                        <SearchBox cname="navbar__right__search" />
                        <Nav className="navbar__right__icons ml-auto">
                            <LinkContainer to="/cart">
                                <Nav.Link href="/cart"><i className="fas fa-shopping-cart"></i>Cart</Nav.Link>
                            </LinkContainer>

                            {
                                userInfo ? (
                                    <NavDropdown title={userInfo.first_name} id='username' className="navbar__items__item">
                                        <LinkContainer to="/profile">
                                            <NavDropdown.Item>Profile</NavDropdown.Item>
                                        </LinkContainer>

                                        <NavDropdown.Item onClick={ logoutHandler }>Logout</NavDropdown.Item>
                                    </NavDropdown>
                                ) : (

                                    <LinkContainer to="/login" >
                                        <Nav.Link><i className="fas fa-user"></i>Login</Nav.Link>
                                    </LinkContainer>
                                )
                                    
                            }

                        </Nav>
                    </Navbar.Collapse>
                    
                </Container>

            </Navbar>
        </header>

    )
}

export default Header
