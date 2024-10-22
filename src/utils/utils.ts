// eslint-disable-next-line @typescript-eslint/no-explicit-any
export function parseData(input: string): any[] {
  // Split by delimiter and filter empty parts
  const parts = input.split('/split/').filter((part) => part.trim());

  return parts
    .map((part) => {
      try {
        // Skip if empty
        if (!part.trim()) {
          return null;
        }

        // If it's a SQL query object, handle it specially
        if (part.includes('sql_query')) {
          const matches = part.match(
            /{.*?'sql_query':\s*'(.*?)'(?:\s*,\s*'sql_valid':\s*(True|False))?\s*}/s,
          );
          if (matches) {
            const sql = matches[1];
            const isValid = matches[2] === 'True';

            return matches[2] ? { sql_query: sql, sql_valid: isValid } : { sql_query: sql };
          }
        }

        // For query result, handle the tuple format
        // if (part.includes('query_result')) {
        //     const match = part.match(/{.*?'query_result':\s*\[\(([\d.]+),\)\]}/);
        //     if (match) {
        //         return {
        //             query_result: [Number(match[1])]
        //         };
        //     }
        // }
        // If it's a query result, just clean it up minimally
        if (part.includes('query_result')) {
          // Basic cleanup without parsing the tuple
          return {
            query_result: part.match(/\[(.*?)\]/s)?.[1] || '',
          };
        }

        // For other parts, handle normal JSON conversion
        const normalized = part
          .replace(/True/g, 'true')
          .replace(/False/g, 'false')
          .replace(/None/g, 'null')
          .replace(/'/g, '"')
          .trim();

        return JSON.parse(normalized);
      } catch (error) {
        console.error('Failed to parse:', {
          original: part,
          error: error instanceof Error ? error.message : String(error),
        });
        return {
          error: `Failed to parse: ${error instanceof Error ? error.message : String(error)}`,
          original: part,
        };
      }
    })
    .filter(Boolean); // Remove null entries
}
