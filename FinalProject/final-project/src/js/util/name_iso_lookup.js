import * as codegrid from 'codegrid-js'

var grid = codegrid.CodeGrid('/data/tiles/')

function getIsoCode(lat, long) {
    return new Promise((resolve, reject) => {
        grid.getCode(lat, long, (error, code) => {
            if (error != null) {
                reject(error)
            }
            resolve(code)
        })
    })
}

export default getIsoCode