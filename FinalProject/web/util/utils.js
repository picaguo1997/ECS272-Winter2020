function getDates(startDate, stopDate) {
    var dateArray = [];
    var currentDate = moment(startDate);
    var stopDate = moment(stopDate);
    while (currentDate <= stopDate) {
        dateArray.push(moment(currentDate).format('M/D/YY'))
        currentDate = moment(currentDate).add(1, 'days');
    }
    return dateArray;
}