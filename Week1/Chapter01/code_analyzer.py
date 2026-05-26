#!/usr/bin/env python3
"""
Code Analyzer using DeepSeek V4-pro API
Analyzes TypeScript code files using DeepSeek's language model
"""

import os
import sys
from pathlib import Path
from typing import Optional
import openai
from dotenv import load_dotenv

class DeepSeekCodeAnalyzer:
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the DeepSeek Code Analyzer
        
        Args:
            api_key: DeepSeek API key. If None, will try to get from environment variable
        """
        self.api_key = api_key or os.getenv('DEEPSEEK_API_KEY')
        if not self.api_key:
            raise ValueError("API key is required. Set DEEPSEEK_API_KEY environment variable or pass api_key parameter")
        self.api_url = "https://api.deepseek.com/v1"
        self.model = "deepseek-v4-pro"  # DeepSeek V4-pro model
        self.client = openai.OpenAI(api_key=self.api_key, base_url=self.api_url)
        
    def read_code_file(self, code_file: str) -> str:
        """Read code from file"""
        try:
            with open(code_file, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {self.code_file}")
        except Exception as e:
            raise Exception(f"Error reading file {self.code_file}: {str(e)}")
    
    def analyze_code(self, code_content: str, file_name: str = "unknown.py") -> str:
        """
        Analyze code using DeepSeek V4-pro API (via OpenAI-compatible client)
        
        Args:
            code_content: The code to analyze
            file_name: Name of the file being analyzed
            
        Returns:
            Analysis result from the API
        """
        prompt = f"""Please analyze the following TypeScript code file: {file_name}

Code to analyze:
```typescript
{code_content}
```     
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                max_tokens=2000
            )
            
            return response.choices[0].message.content
                
        except openai.OpenAIError as e:
            raise Exception(f"DeepSeek API request failed: {str(e)}")
    
    def analyze_file(self, file_path: str) -> str:
        """
        Analyze a TypeScript file
        
        Args:
            file_path: Path to the TypeScript file to analyze
            
        Returns:
            Analysis result
        """
        if not file_path.endswith('.ts'):
            raise ValueError("Only TypeScript files (.ts) are supported")
        
        code_content = self.read_code_file(file_path)
        file_name = Path(file_path).name
        
        print(f"Analyzing file: {file_path}")
        print("=" * 50)
        
        analysis = self.analyze_code(code_content, file_name)
        
        return analysis


def main():
    
    load_dotenv()
    api_key = os.getenv('api_key')
    code_file = os.getenv('code_file')
    
    try:
        analyzer = DeepSeekCodeAnalyzer(api_key)
        analysis = analyzer.analyze_file(code_file)
        
        print("\n" + "=" * 50)
        print("CODE ANALYSIS RESULTS:")
        print("=" * 50)
        print(analysis)
            
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
