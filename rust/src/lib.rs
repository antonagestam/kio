use pyo3::prelude::*;

mod readers;

#[pymodule]
mod _kio_core {
    #[pymodule_export]
    use crate::readers::read_boolean;
    #[pymodule_export]
    use crate::readers::read_compact_string;
    #[pymodule_export]
    use crate::readers::read_compact_string_nullable;
    #[pymodule_export]
    use crate::readers::read_compact_string_as_bytes;
    #[pymodule_export]
    use crate::readers::read_compact_string_as_bytes_nullable;
    #[pymodule_export]
    use crate::readers::read_float64;
    #[pymodule_export]
    use crate::readers::read_int16;
    #[pymodule_export]
    use crate::readers::read_int32;
    #[pymodule_export]
    use crate::readers::read_int64;
    #[pymodule_export]
    use crate::readers::read_int8;
    #[pymodule_export]
    use crate::readers::read_uint16;
    #[pymodule_export]
    use crate::readers::read_uint32;
    #[pymodule_export]
    use crate::readers::read_uint64;
    #[pymodule_export]
    use crate::readers::read_uint8;
    #[pymodule_export]
    use crate::readers::read_unsigned_varint;
}
