#!/usr/bin/env bash
sed -i 's/Amenity/Service/g' "$1"
sed -i 's/amenity/service/g' "$1"
sed -i 's/amenities/services/g' "$1"
sed -i 's/Place/Hospital/g' "$1"
sed -i 's/place/hospital/g' "$1"
sed -i 's/places/hospitals/g' "$1"
