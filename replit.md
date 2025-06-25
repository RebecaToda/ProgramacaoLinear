# Otimização de Produção - Fábrica de Móveis

## Overview

This is a Streamlit-based web application for production optimization in a furniture factory. The application uses linear programming techniques to solve optimization problems related to manufacturing processes. It's designed with a dark theme interface and provides interactive tools for production planning and resource allocation.

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit - A Python-based web framework for building data applications
- **UI Components**: Custom CSS styling with dark theme configuration
- **Layout**: Wide layout with expandable sidebar for controls and parameters
- **Styling**: Custom CSS classes for headers, metrics containers, and warning boxes

### Backend Architecture
- **Language**: Python 3.11
- **Core Libraries**:
  - NumPy for numerical computations
  - Pandas for data manipulation and analysis
  - SciPy for optimization algorithms (specifically `linprog` for linear programming)
- **Framework**: Streamlit for both frontend and backend logic

### Data Processing
- **Optimization Engine**: SciPy's linear programming solver (`linprog`)
- **Data Structures**: NumPy arrays and Pandas DataFrames for handling production data
- **Warning Management**: Configured to suppress unnecessary warnings during optimization

## Key Components

### 1. Main Application (`app.py`)
- **Purpose**: Entry point for the Streamlit application
- **Functionality**: 
  - Sets up page configuration with custom styling
  - Implements production optimization logic
  - Provides interactive interface for parameter input

### 2. Configuration Files
- **Streamlit Config** (`.streamlit/config.toml`): Defines server settings and dark theme
- **Project Config** (`pyproject.toml`): Python project dependencies and metadata
- **Replit Config** (`.replit`): Development environment and deployment settings

### 3. Custom Styling
- **Dark Theme**: Implemented through Streamlit's theme configuration
- **Custom CSS**: Defines styling for headers, containers, and interactive elements
- **Color Scheme**: Primary color (#ff6b6b), dark backgrounds, white text

## Data Flow

1. **User Input**: Parameters entered through Streamlit interface
2. **Data Processing**: NumPy/Pandas handle data manipulation
3. **Optimization**: SciPy's linprog solves linear programming problems
4. **Results Display**: Streamlit renders optimized solutions and visualizations
5. **Interactive Updates**: Real-time recalculation based on parameter changes

## External Dependencies

### Core Dependencies
- **Streamlit (>=1.46.0)**: Web application framework
- **NumPy (>=2.3.1)**: Numerical computing library
- **Pandas (>=2.3.0)**: Data manipulation and analysis
- **SciPy (>=1.16.0)**: Scientific computing and optimization

### Supporting Libraries
- **Altair**: Data visualization (Streamlit dependency)
- **Blinker**: Signal/event system (Streamlit dependency)
- **Cachetools**: Caching utilities (Streamlit dependency)

## Deployment Strategy

### Development Environment
- **Platform**: Replit with Nix package management
- **Python Version**: 3.11
- **Server**: Streamlit development server on port 5000

### Production Deployment
- **Target**: Autoscale deployment (cloud-based)
- **Runtime**: Streamlit server with headless configuration
- **Port**: 5000 with external access
- **Address**: Bound to 0.0.0.0 for external accessibility

### Environment Configuration
- **Nix Channel**: stable-24_05
- **System Packages**: Includes necessary system libraries for numerical computing
- **Python Modules**: Managed through pyproject.toml with uv lock file

## Recent Changes
- June 25, 2025: Sistema de otimização completo implementado
- Máxima Teórica configurada para usar valores contínuos (permite frações)
- Interface totalmente em português brasileiro
- Tema lilás (#a476cf) com fundo escuro (#212021) aplicado
- Sistema de edição de parâmetros funcionando corretamente

## Changelog
- June 25, 2025. Initial setup

## User Preferences

Preferred communication style: Simple, everyday language.