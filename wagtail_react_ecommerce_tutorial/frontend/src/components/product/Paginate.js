import React from 'react'
import { Pagination } from 'react-bootstrap'
import { LinkContainer } from 'react-router-bootstrap'


function Paginate({ pages, page, urlParams='' }) {

    let keyword = ''

    if (urlParams) {

        // Trim keyword to contain only the keyword value
        keyword = urlParams.split('?keyword=')[1].split('&')[0]
    }
    
    return (
        pages > 1 && (

            <Pagination>
                {
                    [...Array(pages).keys()].map( (pageKey) => (

                        <LinkContainer
                            key={pageKey + 1}
                            to={`/?keyword=${keyword}&page=${pageKey + 1}`}
                        >
                            <Pagination.Item active={pageKey + 1 === page}>{ pageKey + 1 }</Pagination.Item>
                        </LinkContainer>
                    ))
                }
            </Pagination>

        )
    )
}

export default Paginate
