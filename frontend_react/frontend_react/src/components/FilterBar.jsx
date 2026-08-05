function FilterBar() {

    return (

        <div className="filter-bar">

            <input
                type="text"
                placeholder="Search transaction..."
            />

            <select>

                <option>Status</option>

                <option>OPEN</option>

                <option>RESOLVED</option>

            </select>

            <select>

                <option>Severity</option>

                <option>HIGH</option>

                <option>MEDIUM</option>

                <option>LOW</option>

            </select>

        </div>

    );

}

export default FilterBar;