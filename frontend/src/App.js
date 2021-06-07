import { Container } from 'react-bootstrap'    // React bootstrap package
import { BrowserRouter as Router, Route } from 'react-router-dom'

import Header from './components/header/Header'
import Footer from './components/footer/Footer'

import HomeScreen from './screens/home/HomeScreen'
import ProductScreen from './screens/product/ProductScreen'
import CartScreen from './screens/cart/CartScreen'
import LoginScreen from './screens/user/LoginScreen'

function App() {

	return (

		<Router>
			<Header />
			
			<main className="py-3">
				<Container>
					<Route path='/' component={ HomeScreen } exact />
					<Route path='/login' component={ LoginScreen } />
					<Route path='/product/:id' component={ ProductScreen } />
					<Route path='/cart/:id?' component={ CartScreen } />
				</Container>
			</main>

			<Footer />
		</Router>

	);
}

export default App;
