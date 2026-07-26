import { useState } from "react";
import API from "./services/api";

function App() {
  const [city, setCity] = useState("");
  const [limit, setLimit] = useState(100);
  const [restaurants, setRestaurants] = useState([]);

  const handleSearch = async () => {
    if (!city.trim()) {
      alert("Please enter a city.");
      return;
    }

    try {
      const response = await API.get("/restaurants", {
        params: {
          city,
          limit,
        },
      });

      setRestaurants(response.data.restaurants);
    } catch (error) {
      console.error(error);
      alert("Failed to fetch restaurants.");
    }
  };

  const handleDownload = () => {
    if (!city.trim()) {
      alert("Please enter a city first.");
      return;
    }

    window.open(
      `http://127.0.0.1:8000/download?city=${encodeURIComponent(
        city
      )}&limit=${limit}`,
      "_blank"
    );
  };

  return (
    <div className="container mt-5">

      <h2 className="text-center mb-4">
        Restaurant Intelligence Platform
      </h2>

      <div className="card p-4 shadow-sm">

        <div className="mb-3">
          <label className="form-label">
            City
          </label>

          <input
            type="text"
            className="form-control"
            placeholder="Enter City"
            value={city}
            onChange={(e) => setCity(e.target.value)}
          />
        </div>

        <div className="mb-3">

          <label className="form-label">
            Number of Restaurants
          </label>

          <select
            className="form-select"
            value={limit}
            onChange={(e) => setLimit(Number(e.target.value))}
          >
            <option value={25}>25</option>
            <option value={50}>50</option>
            <option value={100}>100</option>
          </select>

        </div>

        <button
          className="btn btn-primary"
          onClick={handleSearch}
        >
          Search Restaurants
        </button>

      </div>

      {restaurants.length > 0 && (
        <>
          <h4 className="mt-5">
            Restaurants Found ({restaurants.length})
          </h4>

          <table className="table table-bordered table-striped mt-3">

            <thead className="table-dark">

              <tr>
                <th>#</th>
                <th>Name</th>
                <th>Phone</th>
                <th>Address</th>
                <th>Cuisine</th>
                <th>Google Maps</th>
              </tr>

            </thead>

            <tbody>

              {restaurants.map((restaurant, index) => (

                <tr key={index}>

                  <td>{index + 1}</td>

                  <td>{restaurant.name || "N/A"}</td>

                  <td>{restaurant.phone || "-"}</td>

                  <td>{restaurant.address || "-"}</td>

                  <td>{restaurant.cuisine || "-"}</td>

                  <td>
                    {restaurant.google_maps ? (
                      <a
                        href={restaurant.google_maps}
                        target="_blank"
                        rel="noreferrer"
                      >
                        Open Map
                      </a>
                    ) : (
                      "-"
                    )}
                  </td>

                </tr>

              ))}

            </tbody>

          </table>

          <div className="text-end mt-3">

            <button
              className="btn btn-success"
              onClick={handleDownload}
            >
              Download Excel
            </button>

          </div>

        </>
      )}
    </div>
  );
}

export default App;