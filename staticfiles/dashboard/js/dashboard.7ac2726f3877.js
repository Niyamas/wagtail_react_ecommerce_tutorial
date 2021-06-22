class Dashboard {

    static async getUserList() {
        /**
         * Gets a list of all users in the
         * database from the API.
         */
        console.log('Running getUserList...')

        let domainURL = 'http://localhost:8000'
        let apiURL = domainURL + '/api/v1/users/'

        console.log(apiURL)

        // @ todo: find a way to safely abstract and get the csrf token and JWT token for authorization.
        let config = {
            headers: {
                'Content-type': 'application/json',
                'X-CSRFToken': '9E9ONbS2xpbNgNtdYX3zs0nDou4GTz0c2lKAE0vlqw3SzUO4GYlk4pQQkbDNswc3',
                Authorization: "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjI1MTY5NDI2LCJqdGkiOiIwNzExODBiYmI4YjA0NjMwOTQ4NmE4NThjZWRiYTU2ZSIsInVzZXJfaWQiOjF9.nEFT4pKgL1X4dTpNHdng9-4hwwbdeH7z66NkfuyK5xM"
            }
        }

        let { data } = await axios.get(
            apiURL,
            config
        )
        .catch( (error) => console.log('axios get error:', error) )

        console.log(data)
    }
}

Dashboard.getUserList()