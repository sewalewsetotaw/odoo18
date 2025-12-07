from odoo import http
from odoo.exceptions import AccessError, ValidationError
from odoo.http import request

import json


class PropertyController(http.Controller):

    @http.route('/api/property', type='http', cors="*", auth='user', methods=['GET'], csrf=False)
    def get_property_list(self):
        # 📌 API Endpoint: /api/property
        # type='http'   → Standard HTTP request (not JSON-RPC)
        # cors="*"      → Allow cross-domain requests (frontend/mobile apps)
        # auth='user'   → Only logged-in Odoo users can access
        # methods=['POST'] → Accepts only POST requests (create/send data)
        # csrf=False    → Disable CSRF (needed for external clients)
        #
        # 👉 Common HTTP Methods (for Postman):
        # POST    → Create new property (send data)
        # GET     → Retrieve property/properties
        # PUT     → Replace all fields of property
        # PATCH   → Update part of a property (e.g. price)
        # DELETE  → Remove property record
        # HEAD    → Same as GET but returns only headers
        # OPTIONS → Show allowed methods (used in CORS preflight)
        """Retrieve a list of property records"""
        try:
            # Fetch all property records
            property_records = request.env['property.management'].sudo().search([])

            # Prepare response data
            properties = []
            for record in property_records:
                properties.append({
                    'id': record.id,
                    'name': record.name,
                    'property_type': record.property_type,
                    'price_per_month': record.price_per_month,
                    'status': record.status,
                    'num_bedrooms': record.num_bedrooms,
                    'address': record.address or False,
                    'year_built': record.year_built or False,
                    'area_sqft': record.area_sqft or False,
                    'num_floors': record.num_floors or False,
                    'license_number': record.license_number or False,
                    'discount_percent': record.discount_percent or 0.0,
                    'description': record.description or False,
                    'price_per_year': record.price_per_year or 0.0,
                    'discounted_price': record.discounted_price or 0.0,
                    'currency_id': record.currency_id.id,
                    'company_id': record.company_id.id,
                    'feature_ids': record.feature_ids.ids
                })

            return http.Response(
                json.dumps({'status': 'success', 'data': properties, 'count': len(properties)}),
                content_type='application/json',
                headers={'X-Request-Method': 'GET', 'X-Debug-Info': 'Property list retrieval'},
                status=200
            )

        except Exception as e:
            return http.Response(
                json.dumps({'status': 'error', 'message': f'Unexpected error: {str(e)}'}),
                content_type='application/json',
                status=500
            )

    @http.route('/api/property/<int:property_id>', cors="*", type='http', auth='user', methods=['GET'], csrf=False)
    def get_property(self, property_id, **kwargs):
        """Retrieve a single property record"""
        try:
            # Find the property record
            property_record = request.env['property.management'].sudo().browse(property_id)
            if not property_record.exists():
                return http.Response(
                    json.dumps({'status': 'error', 'message': f'Property with ID {property_id} not found'}),
                    content_type='application/json',
                    status=404
                )

            # Prepare response data
            response_data = {
                'id': property_record.id,
                'name': property_record.name,
                'property_type': property_record.property_type,
                'price_per_month': property_record.price_per_month,
                'status': property_record.status,
                'num_bedrooms': property_record.num_bedrooms,
                'address': property_record.address or False,
                'year_built': property_record.year_built or False,
                'area_sqft': property_record.area_sqft or False,
                'num_floors': property_record.num_floors or False,
                'license_number': property_record.license_number or False,
                'discount_percent': property_record.discount_percent or 0.0,
                'description': property_record.description or False,
                'price_per_year': property_record.price_per_year or 0.0,
                'discounted_price': property_record.discounted_price or 0.0,
                'currency_id': property_record.currency_id.id,
                'company_id': property_record.company_id.id,
                'feature_ids': property_record.feature_ids.ids
            }

            return http.Response(
                json.dumps({'status': 'success', 'data': response_data}),
                content_type='application/json',
                headers={'X-Request-Method': 'GET', 'X-Debug-Info': 'Single property retrieval'},
                status=200
            )

        except Exception as e:
            return http.Response(
                json.dumps({'status': 'error', 'message': f'Unexpected error: {str(e)}'}),
                content_type='application/json',
                status=500
            )

    @http.route('/api/property', type='http', cors="*", auth='user', methods=['POST'], csrf=False)
    def create_property(self, **kwargs):
        try:
            # Extract data from the raw request body
            if not request.httprequest.data:
                return http.Response(
                    json.dumps({'status': 'error', 'message': 'No JSON data provided'}),
                    content_type='application/json',
                    status=400
                )
            try:
                data = json.loads(request.httprequest.data.decode('utf-8')) or {}
            except ValueError:
                return http.Response(
                    json.dumps({'status': 'error', 'message': 'Invalid JSON data'}),
                    content_type='application/json',
                    status=400
                )
            required_fields = ['name', 'property_type', 'price_per_month', 'status', 'num_bedrooms']

            # Validate required fields
            for field in required_fields:
                if field not in data or data[field] is None:
                    return http.Response(
                        json.dumps({'status': 'error', 'message': f'Missing or empty required field: {field}'}),
                        content_type='application/json',
                        status=400
                    )

            # Validate selection fields
            valid_property_types = ['apartment', 'villa', 'office', 'commercial']
            valid_statuses = ['available', 'rented', 'maintenance']
            if data['property_type'] not in valid_property_types:
                return http.Response(
                    json.dumps({'status': 'error',
                                'message': f'Invalid property_type. Must be one of: {", ".join(valid_property_types)}'}),
                    content_type='application/json',
                    status=400
                )
            if data['status'] not in valid_statuses:
                return http.Response(
                    json.dumps({'status': 'error',
                                'message': f'Invalid status. Must be one of: {", ".join(valid_statuses)}'}),
                    content_type='application/json',
                    status=400
                )

            # Calculate discounted_price
            price_per_month = float(data.get('price_per_month'))
            discount_percent = float(data.get('discount_percent', 0.0))
            discounted_price = price_per_month * (1 - discount_percent / 100)

            # Prepare data for creation
            property_data = {
                'name': data.get('name'),
                'property_type': data.get('property_type'),
                'price_per_month': price_per_month,
                'status': data.get('status'),
                'num_bedrooms': int(data.get('num_bedrooms')),
                'address': data.get('address', False),
                'year_built': int(data.get('year_built')) if data.get('year_built') else False,
                'area_sqft': float(data.get('area_sqft')) if data.get('area_sqft') else False,
                'num_floors': int(data.get('num_floors')) if data.get('num_floors') else False,
                'license_number': data.get('license_number', False),
                'discount_percent': discount_percent,
                'description': data.get('description', False),
                'discounted_price': discounted_price,  # Add calculated discounted_price
            }

            property_record = request.env['property.management'].sudo().create(property_data)

            return http.Response(
                json.dumps({
                    'status': 'success',
                    'message': 'Property created successfully',
                    'property_id': property_record.id
                }),
                content_type='application/json',
                headers={'X-Request-Method': 'POST', 'X-Debug-Info': 'Property creation'},
                status=200
            )

        except Exception as e:
            return http.Response(
                json.dumps({'status': 'error', 'message': f'Unexpected error: {str(e)}'}),
                content_type='application/json',
                status=500
            )

    @http.route('/api/property/<int:property_id>', type='http', cors="www.abc.com", auth='public', methods=['PUT'], csrf=False)
    def update_property(self, property_id, **kwargs):
        """Update an existing property record"""
        try:
            # Find the property record
            property_record = request.env['property.management'].sudo().browse(property_id)
            if not property_record.exists():
                return http.Response(
                    json.dumps({'status': 'error', 'message': f'Property with ID {property_id} not found'}),
                    content_type='application/json',
                    status=404
                )

            # Extract data from the raw request body
            if not request.httprequest.data:
                return http.Response(
                    json.dumps({'status': 'error', 'message': 'No JSON data provided'}),
                    content_type='application/json',
                    status=400
                )
            try:
                data = json.loads(request.httprequest.data.decode('utf-8')) or {}
            except ValueError:
                return http.Response(
                    json.dumps({'status': 'error', 'message': 'Invalid JSON data'}),
                    content_type='application/json',
                    status=400
                )

            # Validate selection fields if provided
            valid_property_types = ['apartment', 'villa', 'office', 'commercial']
            valid_statuses = ['available', 'rented', 'maintenance']
            if 'property_type' in data and data['property_type'] not in valid_property_types:
                return http.Response(
                    json.dumps({'status': 'error',
                                'message': f'Invalid property_type. Must be one of: {", ".join(valid_property_types)}'}),
                    content_type='application/json',
                    status=400
                )
            if 'status' in data and data['status'] not in valid_statuses:
                return http.Response(
                    json.dumps(
                        {'status': 'error', 'message': f'Invalid status. Must be one of: {", ".join(valid_statuses)}'}),
                    content_type='application/json',
                    status=400
                )

            # Prepare data for update
            property_data = {}
            if 'name' in data and data['name'] is not None:
                property_data['name'] = data['name']
            if 'property_type' in data and data['property_type'] is not None:
                property_data['property_type'] = data['property_type']
            if 'price_per_month' in data and data['price_per_month'] is not None:
                property_data['price_per_month'] = float(data['price_per_month'])
            if 'status' in data and data['status'] is not None:
                property_data['status'] = data['status']
            if 'num_bedrooms' in data and data['num_bedrooms'] is not None:
                property_data['num_bedrooms'] = int(data['num_bedrooms'])
            if 'address' in data:
                property_data['address'] = data['address']
            if 'year_built' in data:
                property_data['year_built'] = int(data['year_built']) if data['year_built'] is not None else False
            if 'area_sqft' in data:
                property_data['area_sqft'] = float(data['area_sqft']) if data['area_sqft'] is not None else False
            if 'num_floors' in data:
                property_data['num_floors'] = int(data['num_floors']) if data['num_floors'] is not None else False
            if 'license_number' in data:
                property_data['license_number'] = data['license_number']
            if 'discount_percent' in data and data['discount_percent'] is not None:
                property_data['discount_percent'] = float(data['discount_percent'])
            if 'description' in data:
                property_data['description'] = data['description']

            # Calculate discounted_price if price_per_month or discount_percent is provided
            if 'price_per_month' in data or 'discount_percent' in data:
                price_per_month = float(data.get('price_per_month', property_record.price_per_month))
                discount_percent = float(data.get('discount_percent', property_record.discount_percent or 0.0))
                property_data['discounted_price'] = price_per_month * (1 - discount_percent / 100)

            # Update the property record
            # Remove sudo() in production and ensure proper access rights
            property_record.write(property_data)

            return http.Response(
                json.dumps({
                    'status': 'success',
                    'message': f'Property with ID {property_id} updated successfully'
                }),
                content_type='application/json',
                headers={'X-Request-Method': 'PUT', 'X-Debug-Info': 'Property update'},
                status=200
            )
        except (AccessError, ValidationError) as e:
            return http.Response(
                json.dumps({'status': 'error', 'message': str(e)}),
                content_type='application/json',
                status=403
            )
        except ValueError as e:
            return http.Response(
                json.dumps({'status': 'error', 'message': f'Invalid data type: {str(e)}'}),
                content_type='application/json',
                status=400
            )
        except Exception as e:
            return http.Response(
                json.dumps({'status': 'error', 'message': f'Unexpected error: {str(e)}'}),
                content_type='application/json',
                status=500
            )

    @http.route('/api/property/<int:property_id>', type='http', auth='user', methods=['DELETE'], csrf=False)
    def delete_property(self, property_id, **kwargs):
        """Delete a property record"""
        try:
            # Find the property record
            property_record = request.env['property.management'].sudo().browse(property_id)
            if not property_record.exists():
                return http.Response(
                    json.dumps({'status': 'error', 'message': f'Property with ID {property_id} not found'}),
                    content_type='application/json',
                    status=404
                )

            # Delete the property record
            # Remove sudo() in production and ensure proper access rights
            property_record.unlink()

            return http.Response(
                json.dumps({
                    'status': 'success',
                    'message': f'Property with ID {property_id} deleted successfully'
                }),
                content_type='application/json',
                headers={'X-Request-Method': 'DELETE', 'X-Debug-Info': 'Property deletion'},
                status=200
            )
        except (AccessError, ValidationError) as e:
            return http.Response(
                json.dumps({'status': 'error', 'message': str(e)}),
                content_type='application/json',
                status=403
            )
        except Exception as e:
            return http.Response(
                json.dumps({'status': 'error', 'message': f'Unexpected error: {str(e)}'}),
                content_type='application/json',
                status=500
            )