PREFIX = '    version='
REPLACED = /['",\s]/g

/**
 *
 * @param {string} line
 */
function isLineVersion(line) {
    return line.startsWith(PREFIX);
}

module.exports.readVersion = function (contents) {
    const lines = contents.split("\n");
    const line = lines.find(x => isLineVersion(x));
    if (!line) {
        throw new Error('VERSION NOT FOUND');
    }

    return line.replace(PREFIX, '').replace(REPLACED, '').trim()
}

module.exports.writeVersion = function (contents, version) {
    const lines = contents.split("\n");
    lines.forEach((line, index) => {
        if (isLineVersion(line)) {
            lines[index] = `${PREFIX}'${version}',`
        }
    })

    return lines.join("\n");
}
