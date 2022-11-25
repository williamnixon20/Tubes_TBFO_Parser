for (let i = 0; i < 5; i++) {
    if (i == 2) {
        break;
    } else {
        continue;
    }
    throw "ERROR";
}
throw "ERROR";
