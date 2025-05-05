from typing import Dict, List, Any, Tuple

from flask import jsonify, Response

def create_response(
  data: Any = None,
  status: str = "success",
  message: str = "",
  status_code: int = 200
) -> Tuple[Response, int]:
  """
  Create a standardized API response.
  
  Args:
      data: Response data
      status: Status string (success/error)
      message: Message string
      status_code: HTTP status code
      
  Returns:
      JSON response and status code
  """
  response = {
    "status": status,
    "message": message,
    "data": data
  }
  
  return jsonify(response), status_code

def error_response(
  message: str = "An error occurred",
  status_code: int = 400,
  errors: List[str] = None
) -> Tuple[Response, int]:
  """
  Create a standardized error response.
  
  Args:
      message: Error message
      status_code: HTTP status code
      errors: List of error details
      
  Returns:
      JSON response and status code
  """
  response = {
    "status": "error",
    "message": message,
    "errors": errors or []
  }
  
  return jsonify(response), status_code

def parse_request_args(args: Dict, fields: List[str]) -> Dict:
  """
  Parse request arguments into a clean dictionary.
  
  Args:
      args: Request arguments
      fields: Fields to extract
      
  Returns:
      Dictionary with extracted fields
  """
  result = {}
  
  for field in fields:
    if field in args and args[field]:
      result[field] = args[field]
      
  return result

def validate_pagination(page: str, per_page: str) -> Tuple[int, int]:
  """
  Validate and parse pagination parameters.
  
  Args:
      page: Page number string
      per_page: Items per page string
      
  Returns:
      Tuple of (page, per_page) as integers
  """
  try:
    page_num = int(page) if page else 1
  except ValueError:
    page_num = 1
    
  try:
    per_page_num = int(per_page) if per_page else 10
  except ValueError:
    per_page_num = 10
    
  # Ensure reasonable values
  page_num = max(1, page_num)
  per_page_num = max(1, min(100, per_page_num))
  
  return page_num, per_page_num 