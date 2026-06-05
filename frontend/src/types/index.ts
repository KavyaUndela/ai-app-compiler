export interface Entity {
  name: string
  entity_type: string
  description?: string
}

export interface Feature {
  name: string
  description: string
  related_entities: string[]
}

export interface Role {
  name: string
  permissions: string[]
  description?: string
}

export interface IntentSchema {
  intent_id: string
  entities: Entity[]
  features: Feature[]
  roles: Role[]
  workflows: string[]
  summary: string
}

export interface PageSchema {
  name: string
  component_type: string
  fields: string[]
  required_roles: string[]
}

export interface Module {
  name: string
  pages: PageSchema[]
  functions: string[]
}

export interface SystemDesignSchema {
  design_id: string
  modules: Module[]
  navigation: Record<string, string[]>
  auth_flow: string
  user_workflows: string[]
  summary: string
}

export interface DatabaseField {
  name: string
  field_type: string
  nullable: boolean
  primary_key: boolean
  unique: boolean
}

export interface DatabaseTable {
  table_name: string
  fields: DatabaseField[]
  indexes: string[]
}

export interface APIEndpoint {
  method: string
  path: string
  description: string
  required_roles: string[]
  request_body?: Record<string, any>
  response_body: Record<string, any>
}

export interface SchemaGenerationResult {
  schema_id: string
  database_schema: DatabaseTable[]
  api_schema: APIEndpoint[]
  ui_schema: Record<string, any>
  auth_schema: Record<string, any>
}

export interface ValidationIssue {
  issue_id: string
  severity: string
  category: string
  message: string
  affected_component: string
  suggestion?: string
}

export interface ValidationResult {
  validation_id: string
  schema_id: string
  issues: ValidationIssue[]
  is_valid: boolean
  summary: string
}

export interface RepairPatch {
  patch_id: string
  affected_component: string
  original_value: any
  fixed_value: any
  explanation: string
  confidence: number
}

export interface RepairResult {
  repair_id: string
  validation_id: string
  patches: RepairPatch[]
  repaired_schema?: SchemaGenerationResult
  summary: string
}

export interface FormField {
  name: string
  label: string
  field_type: string
  required: boolean
  options?: string[]
}

export interface FormSchema {
  form_id: string
  title: string
  description: string
  fields: FormField[]
  submit_action: string
}

export interface CRUDPage {
  page_id: string
  entity_name: string
  list_columns: string[]
  create_form: FormSchema
  edit_form: FormSchema
  delete_confirmation: string
}

export interface RuntimePreview {
  preview_id: string
  schema_id: string
  dynamic_forms: FormSchema[]
  crud_pages: CRUDPage[]
  preview_html?: string
  sample_data: Record<string, any[]>
}

export interface CompilationResult {
  compilation_id: string
  original_prompt: string
  intent: IntentSchema
  design: SystemDesignSchema
  schema: SchemaGenerationResult
  validation: ValidationResult
  repair?: RepairResult
  runtime_preview: RuntimePreview
  status: string
  summary: string
}
