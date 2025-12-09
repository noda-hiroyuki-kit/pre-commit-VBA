"""Test module for IVbComponentType class."""

import pytest

from pre_commit_vba import (
    ClassModule,
    SheetClassModule,
    StdModule,
    UndefineTypeError,
    UserFormModule,
    constants,
    vb_component_type_factory,
)


class TestVbComponentType:
    """Tests for IVbComponentType class."""

    class TestConstructVbComponentType:
        """Tests for construct IVbComponentType."""

        @pytest.mark.parametrize(
            ("module_name", "type_id", "expected_class"),
            [
                ("Module1", 1, StdModule),
                ("Class1", 2, ClassModule),
                ("UserForm1", 3, UserFormModule),
                ("Sheet1", 100, SheetClassModule),
            ],
        )
        def test_vb_component_type_factory(
            self,
            module_name: str,
            type_id: int,
            expected_class: type,
        ) -> None:
            """Test vb_component_type_factory returns correct instance."""
            vb_component = vb_component_type_factory(module_name, type_id)
            assert isinstance(vb_component, expected_class)  # noqa: S101

        def test_vb_component_type_factory_invalid_type(self) -> None:
            """Test vb_component_type_factory raises ValueError for invalid type_id."""
            with pytest.raises(UndefineTypeError) as exc_info:
                vb_component_type_factory("InvalidModule", 999)
            assert "999" in str(exc_info.value)  # noqa: S101


@pytest.mark.develop_research
class TestConstants:
    """Tests for VbComponentType constants."""

    def test_vbext_ct_std_module_is_1(self) -> None:
        """Test that VbComponentType constants have expected values."""
        assert constants.vbext_ct_StdModule == 1  # noqa: S101

    def test_vbext_ct_class_module_is_2(self) -> None:
        """Test that VbComponentType constants have expected values."""
        assert constants.vbext_ct_ClassModule == 2  # noqa: PLR2004, S101

    def test_vbext_ct_msform_is_3(self) -> None:
        """Test that VbComponentType constants have expected values."""
        assert constants.vbext_ct_MSForm == 3  # noqa: PLR2004, S101

    def test_vbext_ct_document_is_100(self) -> None:
        """Test that VbComponentType constants have expected values."""
        assert constants.vbext_ct_Document == 100  # noqa: PLR2004, S101

    def test_cannot_change_vbext_ct_std_module_is_1(self) -> None:
        """Test overwrite constants."""
        with pytest.raises(Exception):  # noqa: B017, PT011
            constants.vbext_ct_StdModule = 20  # type: ignore  # noqa: PGH003
