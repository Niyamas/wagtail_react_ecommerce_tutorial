import { Container } from 'react-bootstrap'    // React bootstrap package
import { BrowserRouter as Router, Route } from 'react-router-dom'

import Header from './components/header/Header'
import Footer from './components/footer/Footer'

import HomeScreen from './screens/home/HomeScreen'
import LoginScreen from './screens/user/LoginScreen'
import RegisterScreen from './screens/user/RegisterScreen'
import ProfileScreen from './screens/user/ProfileScreen'
import ProductScreen from './screens/product/ProductScreen'
import CartScreen from './screens/cart/CartScreen'
import ShippingScreen from './screens/cart/ShippingScreen'
import PaymentScreen from './screens/cart/PaymentScreen'
import PlaceOrderScreen from './screens/cart/PlaceOrderScreen'



function App() {

	return (

		<Router>
			<Header />
			
			<main className="py-3">
				<Container>
					<Route path='/' component={ HomeScreen } exact />
					<Route path='/login' component={ LoginScreen } />
					<Route path='/register' component={ RegisterScreen } />
					<Route path='/profile' component={ ProfileScreen } />
					<Route path='/product/:id' component={ ProductScreen } />
					<Route path='/cart/:id?' component={ CartScreen } />
					<Route path='/shipping' component={ ShippingScreen } />
					<Route path='/payment' component={ PaymentScreen } />
					<Route path='/place-order' component={ PlaceOrderScreen } />
				</Container>
			</main>

			<Footer />
		</Router>

	);
}

export default App;
