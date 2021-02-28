

std::string encode(std::vector<ll> points) {
    //a place to keep the output
    std::string output;
    //unless the shape is very course you should probably only need about 3 bytes
    //per coord, which is 6 bytes with 2 coords, so we overshoot to 8 just in case
    output.reserve(points.size() * 8);

    //handy lambda to turn an integer into an encoded string
    auto serialize = [&output](int number) {
        //move the bits left 1 position and flip all the bits if it was a negative number
        number = number < 0 ? ~(number << 1) : (number << 1);
        //write 5 bit chunks of the number
        while (number >= 0x20) {
            int nextValue = (0x20 | (number & 0x1f)) + 63;
            output.push_back(static_cast<char>(nextValue));
            number >>= 5;
        }
        //write the last chunk
        number += 63;
        output.push_back(static_cast<char>(number));
    };

    //this is an offset encoding so we remember the last point we saw
    int last_lon = 0, last_lat = 0;
    //for each point
    for (const auto& p : points) {
        //shift the decimal point 5 places to the right and truncate
        int lon = static_cast<int>(floor(static_cast<double>(p.lng) * 1e6));
        int lat = static_cast<int>(floor(static_cast<double>(p.lat) * 1e6));
        //encode each coordinate, lat first for some reason
        serialize(lat - last_lat);
        serialize(lon - last_lon);
        //remember the last one we encountered
        last_lon = lon;
        last_lat = lat;
    }
    return output;
}