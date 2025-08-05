"""Tests for the scope system."""

import pytest
from needy import (
    BaseScope, ScopeType, PytestScope, FastAPIScope,
    has_parents, root, ScopeDeclaration, BoundScopeDefinition
)


class TestScopeDeclaration:
    """Test ScopeDeclaration functionality."""
    
    def test_root_creation(self):
        """Test creating a root scope declaration."""
        decl = root()
        assert isinstance(decl, ScopeDeclaration)
        assert decl.direct_parents == []
    
    def test_has_parents_creation(self):
        """Test creating a scope declaration with parents."""
        parent1 = root()
        parent2 = root()
        decl = has_parents(parent1, parent2)
        assert isinstance(decl, ScopeDeclaration)
        assert len(decl.direct_parents) == 2
        assert parent1 in decl.direct_parents
        assert parent2 in decl.direct_parents
    
    def test_set_name(self):
        """Test that __set_name__ sets the name correctly."""
        decl = root()
        decl.__set_name__(None, "TEST_SCOPE")
        assert decl.name == "TEST_SCOPE"
    
    def test_str_representation(self):
        """Test string representation of scope declarations."""
        decl = root()
        decl.__set_name__(None, "TEST_SCOPE")
        assert str(decl) == "TEST_SCOPE"
        assert "TEST_SCOPE" in repr(decl)
    
    def test_descriptor_protocol(self):
        """Test that ScopeDeclaration works as a descriptor."""
        # Create a test class with a scope declaration
        class TestScope(BaseScope):
            TEST = root()
        
        # When accessed on the class, it should return a BoundScopeDefinition
        assert isinstance(TestScope.TEST, BoundScopeDefinition)
        assert TestScope.TEST.name == "TEST"
        assert TestScope.TEST.scope_class == TestScope
        
        # When accessed on an instance, it should also return a BoundScopeDefinition
        test_instance = TestScope()
        assert isinstance(test_instance.TEST, BoundScopeDefinition)
        assert test_instance.TEST.name == "TEST"
        assert test_instance.TEST.scope_class == TestScope
        
        # When accessed directly on the descriptor, it should return self
        test_decl = TestScope.__dict__['TEST']
        assert isinstance(test_decl, ScopeDeclaration)
        assert test_decl.name == "TEST"


class TestBoundScopeDefinition:
    """Test BoundScopeDefinition functionality."""
    
    def test_creation(self):
        """Test creating a bound scope definition."""
        decl = root()
        decl.__set_name__(None, "TEST")
        bound = BoundScopeDefinition(ScopeType, "TEST", decl)
        assert bound.scope_class == ScopeType
        assert bound.name == "TEST"
        assert bound.declaration == decl
    
    def test_str_representation(self):
        """Test string representation of bound scope definitions."""
        decl = root()
        decl.__set_name__(None, "TEST")
        bound = BoundScopeDefinition(ScopeType, "TEST", decl)
        assert str(bound) == "ScopeType.TEST"
        assert "<ScopeType.TEST>" in repr(bound)
    
    def test_equality(self):
        """Test equality of bound scope definitions."""
        decl1 = root()
        decl1.__set_name__(None, "TEST1")
        decl2 = root()
        decl2.__set_name__(None, "TEST2")
        
        bound1 = BoundScopeDefinition(ScopeType, "TEST1", decl1)
        bound2 = BoundScopeDefinition(ScopeType, "TEST1", decl1)
        bound3 = BoundScopeDefinition(ScopeType, "TEST2", decl2)
        bound4 = BoundScopeDefinition(PytestScope, "TEST1", decl1)
        
        assert bound1 == bound2
        assert bound1 != bound3
        assert bound1 != bound4
        assert hash(bound1) == hash(bound2)
    
    def test_hashable(self):
        """Test that bound scope definitions are hashable."""
        decl = root()
        decl.__set_name__(None, "TEST")
        bound = BoundScopeDefinition(ScopeType, "TEST", decl)
        scope_set = {bound}
        assert bound in scope_set


class TestScopeType:
    """Test ScopeType functionality."""
    
    def test_scope_values(self):
        """Test that scope values are bound scope definitions."""
        assert isinstance(ScopeType.SINGLETON, BoundScopeDefinition)
        assert isinstance(ScopeType.REQUEST, BoundScopeDefinition)
        assert isinstance(ScopeType.SESSION, BoundScopeDefinition)
        
        assert ScopeType.SINGLETON.name == "SINGLETON"
        assert ScopeType.REQUEST.name == "REQUEST"
        assert ScopeType.SESSION.name == "SESSION"
    
    def test_singleton_is_root(self):
        """Test that SINGLETON has no parents."""
        assert len(ScopeType.SINGLETON.get_direct_parents()) == 0
        assert len(ScopeType.SINGLETON.get_valid_parents()) == 0
    
    def test_request_parents(self):
        """Test that REQUEST has SINGLETON as parent."""
        parents = ScopeType.REQUEST.get_direct_parents()
        assert len(parents) == 1
        assert ScopeType.SINGLETON in parents
    
    def test_session_parents(self):
        """Test that SESSION has REQUEST as parent."""
        parents = ScopeType.SESSION.get_direct_parents()
        assert len(parents) == 1
        assert ScopeType.REQUEST in parents
    
    def test_session_all_parents(self):
        """Test that SESSION has both REQUEST and SINGLETON as valid parents."""
        all_parents = ScopeType.SESSION.get_valid_parents()
        assert len(all_parents) == 2
        assert ScopeType.REQUEST in all_parents
        assert ScopeType.SINGLETON in all_parents


class TestPytestScope:
    """Test PytestScope functionality."""
    
    def test_scope_values(self):
        """Test that all pytest scope values are bound scope definitions."""
        scopes = [
            PytestScope.SESSION, PytestScope.PACKAGE, PytestScope.MODULE,
            PytestScope.CLASS, PytestScope.DEFINITION, PytestScope.FUNCTION,
            PytestScope.SUBTEST
        ]
        for scope in scopes:
            assert isinstance(scope, BoundScopeDefinition)
    
    def test_session_is_root(self):
        """Test that SESSION has no parents."""
        assert len(PytestScope.SESSION.get_direct_parents()) == 0
        assert len(PytestScope.SESSION.get_valid_parents()) == 0
    
    def test_package_parents(self):
        """Test that PACKAGE has SESSION as parent."""
        parents = PytestScope.PACKAGE.get_direct_parents()
        assert len(parents) == 1
        assert PytestScope.SESSION in parents
    
    def test_module_parents(self):
        """Test that MODULE has PACKAGE as parent."""
        parents = PytestScope.MODULE.get_direct_parents()
        assert len(parents) == 1
        assert PytestScope.PACKAGE in parents
    
    def test_class_parents(self):
        """Test that CLASS has MODULE as parent."""
        parents = PytestScope.CLASS.get_direct_parents()
        assert len(parents) == 1
        assert PytestScope.MODULE in parents
    
    def test_definition_parents(self):
        """Test that DEFINITION has CLASS as parent."""
        parents = PytestScope.DEFINITION.get_direct_parents()
        assert len(parents) == 1
        assert PytestScope.CLASS in parents
    
    def test_function_parents(self):
        """Test that FUNCTION has DEFINITION as parent."""
        parents = PytestScope.FUNCTION.get_direct_parents()
        assert len(parents) == 1
        assert PytestScope.DEFINITION in parents
    
    def test_subtest_parents(self):
        """Test that SUBTEST has FUNCTION as parent."""
        parents = PytestScope.SUBTEST.get_direct_parents()
        assert len(parents) == 1
        assert PytestScope.FUNCTION in parents
    
    def test_function_all_parents(self):
        """Test that FUNCTION has all higher scopes as valid parents."""
        all_parents = PytestScope.FUNCTION.get_valid_parents()
        expected_parents = {
            PytestScope.DEFINITION, PytestScope.CLASS, PytestScope.MODULE,
            PytestScope.PACKAGE, PytestScope.SESSION
        }
        assert all_parents == expected_parents
    
    def test_subtest_all_parents(self):
        """Test that SUBTEST has all higher scopes as valid parents."""
        all_parents = PytestScope.SUBTEST.get_valid_parents()
        expected_parents = {
            PytestScope.FUNCTION, PytestScope.DEFINITION, PytestScope.CLASS,
            PytestScope.MODULE, PytestScope.PACKAGE, PytestScope.SESSION
        }
        assert all_parents == expected_parents


class TestFastAPIScope:
    """Test FastAPIScope functionality."""
    
    def test_scope_values(self):
        """Test that all FastAPI scope values are bound scope definitions."""
        scopes = [
            FastAPIScope.APPLICATION, FastAPIScope.REQUEST,
            FastAPIScope.BACKGROUND_TASK
        ]
        for scope in scopes:
            assert isinstance(scope, BoundScopeDefinition)
    
    def test_application_is_root(self):
        """Test that APPLICATION has no parents."""
        assert len(FastAPIScope.APPLICATION.get_direct_parents()) == 0
        assert len(FastAPIScope.APPLICATION.get_valid_parents()) == 0
    
    def test_request_parents(self):
        """Test that REQUEST has APPLICATION as parent."""
        parents = FastAPIScope.REQUEST.get_direct_parents()
        assert len(parents) == 1
        assert FastAPIScope.APPLICATION in parents
    
    def test_background_task_parents(self):
        """Test that BACKGROUND_TASK has APPLICATION as parent."""
        parents = FastAPIScope.BACKGROUND_TASK.get_direct_parents()
        assert len(parents) == 1
        assert FastAPIScope.APPLICATION in parents
    
    def test_request_all_parents(self):
        """Test that REQUEST has APPLICATION as valid parent."""
        all_parents = FastAPIScope.REQUEST.get_valid_parents()
        assert len(all_parents) == 1
        assert FastAPIScope.APPLICATION in all_parents


class TestScopeHierarchy:
    """Test scope hierarchy functionality."""
    
    def test_scope_comparison(self):
        """Test that scopes can be compared."""
        assert ScopeType.SINGLETON == ScopeType.SINGLETON
        assert ScopeType.SINGLETON != ScopeType.REQUEST
        assert PytestScope.SESSION != FastAPIScope.APPLICATION
    
    def test_scope_hashable(self):
        """Test that scopes are hashable and can be used in sets."""
        scope_set = {ScopeType.SINGLETON, ScopeType.REQUEST, PytestScope.SESSION}
        assert len(scope_set) == 3
        assert ScopeType.SINGLETON in scope_set
    
    def test_parent_validation(self):
        """Test that parent relationships are correctly validated."""
        # REQUEST should have SINGLETON as parent
        assert ScopeType.SINGLETON in ScopeType.REQUEST.get_direct_parents()
        
        # SESSION should have REQUEST as direct parent and SINGLETON as indirect
        assert ScopeType.REQUEST in ScopeType.SESSION.get_direct_parents()
        assert ScopeType.SINGLETON in ScopeType.SESSION.get_valid_parents()
        assert ScopeType.SINGLETON not in ScopeType.SESSION.get_direct_parents()
    
    def test_scope_isolation(self):
        """Test that different scope types are isolated."""
        # PytestScope and FastAPIScope should be separate
        assert PytestScope.SESSION != FastAPIScope.APPLICATION
        assert PytestScope.SESSION.scope_class != FastAPIScope.APPLICATION.scope_class


class TestScopeDeclarationIntegration:
    """Test integration between ScopeDeclaration and scope classes."""
    
    def test_declaration_names_are_set(self):
        """Test that ScopeDeclaration names are properly set in scope classes."""
        # Check that bound scope definitions have correct names
        assert ScopeType.SINGLETON.name == 'SINGLETON'
        assert ScopeType.REQUEST.name == 'REQUEST'
        assert ScopeType.SESSION.name == 'SESSION'
    
    def test_parent_references_are_valid(self):
        """Test that parent references in declarations are valid."""
        # Check that REQUEST has SINGLETON as parent
        request_parents = ScopeType.REQUEST.get_direct_parents()
        assert len(request_parents) == 1
        assert ScopeType.SINGLETON in request_parents
        
        # Check that SESSION has REQUEST as parent
        session_parents = ScopeType.SESSION.get_direct_parents()
        assert len(session_parents) == 1
        assert ScopeType.REQUEST in session_parents 