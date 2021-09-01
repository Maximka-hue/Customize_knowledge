use pyo3::prelude::*;
use pyo3::types::IntoPyDict;

fn main() {
#[pyfunction]
fn double(x: usize) -> usize {
        x * 2
}
/// This module is implemented in Rust.
#[pymodule]
#[pyo3(name = "fast_traverse_url")]
fn my_extension(py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(double, m)?)?;
Ok(())
}
}