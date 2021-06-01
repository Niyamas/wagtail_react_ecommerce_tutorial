import { Container } from 'react-bootstrap'    // React bootstrap package

import Header from './components/header/Header'
import Footer from './components/footer/Footer'
import HomeScreen from './screens/HomeScreen'

function App() {

	return (

		<div className="App">
			<Header />
			
			<main className="py-3">
				<Container>
					<HomeScreen />
				</Container>
			</main>

			<Footer />
		</div>

	);
}

export default App;
