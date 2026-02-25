This is a [Next.js](https://nextjs.org) project bootstrapped with [`create-next-app`](https://nextjs.org/docs/app/api-reference/cli/create-next-app).

## Getting Started

First, run the development server:

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
# or
bun dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

You can start editing the page by modifying `app/page.tsx`. The page auto-updates as you edit the file.

This project uses [`next/font`](https://nextjs.org/docs/app/building-your-application/optimizing/fonts) to automatically optimize and load [Geist](https://vercel.com/font), a new font family for Vercel.

## Learn More

To learn more about Next.js, take a look at the following resources:

- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API.
- [Learn Next.js](https://nextjs.org/learn) - an interactive Next.js tutorial.

You can check out [the Next.js GitHub repository](https://github.com/vercel/next.js) - your feedback and contributions are welcome!

## Deploy on Vercel

The easiest way to deploy your Next.js app is to use the [Vercel Platform](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme) from the creators of Next.js.

Check out our [Next.js deployment documentation](https://nextjs.org/docs/app/building-your-application/deploying) for more details.


## Deploy via AWS Amplify

Simply run git push to the main branch and it will automatically deploy to AWS via AWS Amplify.
Login through the AWS console to monitor the progress of the deployment

---

## Deploying Lambda Functions

The backend is made up of three AWS Lambda functions in `ap-southeast-2`. Each has a PowerShell deploy script that packages and uploads the function code.

### Prerequisites

- [AWS CLI](https://aws.amazon.com/cli/) installed and configured (`aws configure`)
- Python and `pip` installed and available on your PATH
- Your AWS credentials must have `lambda:UpdateFunctionCode` permission

### send-email

Handles sending emails with optional PDF attachments via SES.

```powershell
cd ..\email-api
.\deploy.ps1
```

The script zips `sendemail.py` and uploads it to the `send-email` Lambda function. No external dependencies are needed as `boto3` is built into the Lambda runtime.

### create-invoice-subway

Generates rental invoice PDFs using ReportLab.

```powershell
cd ..\subway-invoice-generator
.\deploy.ps1
```

The script installs `reportlab` locally into a `build/` folder, bundles it with `subway.py`, zips everything, and uploads it to the `create-invoice-subway` Lambda function. The build folder is automatically removed after deployment.

### create-invoice-kfc

Generates KFC rental invoice PDFs using ReportLab.

```powershell
cd ..\kfc-invoice-generator
.\deploy.ps1
```

The script installs `reportlab` locally into a `build/` folder, bundles it with `kfc.py`, zips everything, and uploads it to the `create-invoice-kfc` Lambda function. The build folder is automatically removed after deployment.

> **Note:** Once the Lambda function is created in AWS, you will also need to add a new API Gateway route (e.g. `/kfc-invoice`) pointing to it, matching the pattern used by `/subway-invoice`.

### Verifying a Deployment

After running a deploy script, confirm the deployment worked by checking the **Last modified** timestamp in the AWS Lambda console, or by running the corresponding test script:

```bash
# Test send-email
python ..\email-api\sendemail-test-aws-call.py

# Test create-invoice-subway
python ..\subway-invoice-generator\test-subway-invoice-generator-aws-call.py

# Test create-invoice-kfc
python ..\kfc-invoice-generator\test-kfc-invoice-generator-aws-call.py
```
