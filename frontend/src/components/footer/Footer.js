import React from 'react'
import { Container, Row, Col } from 'react-bootstrap'

import './css/footer.css'

function Footer() {

    return (

        <footer className="footer">
            <div className="footer__content">
                <h1 className="footer__content__title">Brickshop Bazaar</h1>
                <p className="footer__content__copyright">
                    Copyright &copy; Brickshop Emporioum
                </p>
            </div>

        </footer>

    )
}

export default Footer
