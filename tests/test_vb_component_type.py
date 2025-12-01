"""Test module for IVbComponentType class."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Generator

import pytest
from win32com.client import constants, gencache, makepy

from pre_commit_vba import (
    ClassModule,
    SheetClassModule,
    StdModule,
    UndefineTypeError,
    UserFormModule,
    vb_component_type_factory,
)


@pytest.fixture(scope="module", name="arrange_excel_app")
def arrange_excel_app() -> Generator[None]:
    """Arrange Excel Application for tests."""
    excel_app = gencache.EnsureDispatch("Excel.Application")
    makepy.GenerateFromTypeLibSpec(
        "Microsoft Visual Basic for Applications Extensibility 5.3"
    )
    yield
    excel_app.Quit()


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
            arrange_excel_app: Generator,  # noqa: ARG002
            module_name: str,
            type_id: int,
            expected_class: type,
        ) -> None:
            """Test vb_component_type_factory returns correct instance."""
            vb_component = vb_component_type_factory(module_name, type_id)
            assert isinstance(vb_component, expected_class)  # noqa: S101

        def test_vb_component_type_factory_invalid_type(
            self,
            arrange_excel_app: Generator,  # noqa: ARG002
        ) -> None:
            """Test vb_component_type_factory raises ValueError for invalid type_id."""
            with pytest.raises(UndefineTypeError) as exc_info:
                vb_component_type_factory("InvalidModule", 999)
            assert "999" in str(exc_info.value)  # noqa: S101


@pytest.mark.develop_research
class TestConstants:
    """Tests for VbComponentType constants."""

    def test_vbext_ct_std_module_is_1(self, arrange_excel_app: Generator) -> None:  # noqa: ARG002
        """Test that VbComponentType constants have expected values."""
        assert constants.vbext_ct_StdModule == 1  # noqa: S101

    def test_vbext_ct_class_module_is_2(self, arrange_excel_app: Generator) -> None:  # noqa: ARG002
        """Test that VbComponentType constants have expected values."""
        assert constants.vbext_ct_ClassModule == 2  # noqa: PLR2004, S101

    def test_vbext_ct_msform_is_3(self, arrange_excel_app: Generator) -> None:  # noqa: ARG002
        """Test that VbComponentType constants have expected values."""
        assert constants.vbext_ct_MSForm == 3  # noqa: PLR2004, S101

    def test_vbext_ct_document_is_100(self, arrange_excel_app: Generator) -> None:  # noqa: ARG002
        """Test that VbComponentType constants have expected values."""
        assert constants.vbext_ct_Document == 100  # noqa: PLR2004, S101
