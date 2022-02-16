const tracker = {
    filename: 'setup.py',
    updater: require('./standard-version-updater')
}

module.exports = {
    bumpFiles: [tracker],
    packageFiles: [tracker],
}
